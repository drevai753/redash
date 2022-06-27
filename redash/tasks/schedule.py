from __future__ import absolute_import
import logging
import hashlib
import json
from datetime import datetime, timedelta
import calendar

from rq.job import Job
from rq_scheduler import Scheduler

from redash import extensions, settings, rq_redis_connection, statsd_client
from redash.tasks import (
    clear_old_user_history,
    sync_user_details,
    refresh_queries,
    remove_ghost_locks,
    empty_schedules,
    refresh_schemas,
    cleanup_query_results,
    version_check,
    send_aggregated_errors,
    Queue,
)

logger = logging.getLogger(__name__)

def to_unix(dt):
    """Converts a datetime object to unixtime"""
    return calendar.timegm(dt.utctimetuple())

class StatsdRecordingScheduler(Scheduler):
    """
    RQ Scheduler Mixin that uses Redash's custom RQ Queue class to increment/modify metrics via Statsd
    """

    queue_class = Queue
    
    def __init__(self, **kwargs):
        super(StatsdRecordingScheduler, self).__init__(**kwargs)
        self.persistent_jobs = {}
    
    def enqueue_jobs(self):
        self.log.debug("Checking for scheduled jobs")

        jobs = self.get_jobs_to_queue()
        lost_ids = [id for id in self.persistent_jobs]
        for job in jobs:
            self.enqueue_job(job)
        present = self.connection.zrangebyscore(self.scheduled_jobs_key, 0, "+inf")
        logger.info("Found scheduled jobs: {}".format(present))
        for job_id in self.persistent_jobs:
            if bytes(job_id, "utf-8") in present and job_id in lost_ids:
                lost_ids.remove(job_id)
        logger.info("Found lost jobs: {}".format(lost_ids))
        for id in lost_ids:
            try:
                job = self.persistent_jobs[id]
                interval = job.meta.get("interval", None)
                self.connection.zadd(self.scheduled_jobs_key, {job.id: to_unix(datetime.utcnow()) + int(interval)})
                jobs.append(job)
            except Exception as e:
                logger.warn("Failed to schedule job. Id={}  --  {}".format(id, e))
                
        return jobs

    def schedule(self, scheduled_time, id, **kwargs):
        jobs = self.get_jobs()
        job = None
        for j in jobs:
            if j.id == id:
                job = j
                break
        if job is None:
            job = super(StatsdRecordingScheduler, self).schedule(scheduled_time=scheduled_time, id=id, **kwargs)
        if job.meta.get("interval", None) is not None and job.meta.get("repeat", None) is None:
            self.persistent_jobs[job.id] = job
            logger.info("Scheduled persistent job: {}".format(job))
        return job


rq_scheduler = StatsdRecordingScheduler(
    connection=rq_redis_connection, queue_name="periodic", interval=5
)


def job_id(kwargs):
    metadata = kwargs.copy()
    metadata["func"] = metadata["func"].__name__

    return hashlib.sha1(json.dumps(metadata, sort_keys=True).encode()).hexdigest()


def prep(kwargs):
    interval = kwargs["interval"]
    if isinstance(interval, timedelta):
        interval = int(interval.total_seconds())

    kwargs["interval"] = interval
    kwargs["result_ttl"] = kwargs.get("result_ttl", interval * 2)

    return kwargs


def schedule(kwargs):
    rq_scheduler.schedule(scheduled_time=datetime.utcnow(), id=job_id(kwargs), **kwargs)


def periodic_job_definitions():
    jobs = [
        {"func": refresh_queries, "timeout": 600, "interval": 30, "result_ttl": 600},
        {
            "func": remove_ghost_locks,
            "interval": timedelta(minutes=1),
            "result_ttl": 600,
        },
        {"func": empty_schedules, "interval": timedelta(minutes=60)},
        {
            "func": refresh_schemas,
            "interval": timedelta(minutes=settings.SCHEMAS_REFRESH_SCHEDULE),
        },      
        {
            "func": sync_user_details,
            "timeout": 60,
            "interval": timedelta(minutes=1),
            "result_ttl": 600,
        },
        {
            "func": clear_old_user_history,
            "interval": timedelta(days=1),
        },
        {
            "func": send_aggregated_errors,
            "interval": timedelta(minutes=settings.SEND_FAILURE_EMAIL_INTERVAL),
        },
    ]

    if settings.VERSION_CHECK:
        jobs.append({"func": version_check, "interval": timedelta(days=1)})

    if settings.QUERY_RESULTS_CLEANUP_ENABLED:
        jobs.append({"func": cleanup_query_results, "interval": timedelta(minutes=5)})

    # Add your own custom periodic jobs in your dynamic_settings module.
    jobs.extend(settings.dynamic_settings.periodic_jobs() or [])

    # Add periodic jobs that are shipped as part of Redash extensions
    extensions.load_periodic_jobs(logger)
    jobs.extend(list(extensions.periodic_jobs.values()))

    return jobs


def schedule_periodic_jobs(jobs):
    job_definitions = [prep(job) for job in jobs]

    jobs_to_clean_up = Job.fetch_many(
        set([job.id for job in rq_scheduler.get_jobs()])
        - set([job_id(job) for job in job_definitions]),
        rq_redis_connection,
    )

    jobs_to_schedule = [
        job for job in job_definitions
    ]

    for job in jobs_to_clean_up:
        logger.info("Removing %s (%s) from schedule.", job.id, job.func_name)
        rq_scheduler.cancel(job)
        job.delete()

    for job in jobs_to_schedule:
        logger.info(
            "Scheduling %s (%s) with interval %s.",
            job_id(job),
            job["func"].__name__,
            job.get("interval"),
        )
        schedule(job)
