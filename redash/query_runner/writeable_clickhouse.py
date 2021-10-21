import logging

from redash.query_runner import register
from redash.query_runner.clickhouse import ClickHouse
from redash.utils import json_dumps

import requests

logger = logging.getLogger(__name__)

class WriteableClickHouse(ClickHouse):
    @classmethod
    def type(cls):
        return "writeable_clickhouse"

    def _send_query(self, data, stream=False):
        url = self.configuration.get("url", "http://127.0.0.1:8123")
        try:
            verify = self.configuration.get("verify", True)
            r = requests.post(
                url,
                data=data.encode("utf-8","ignore"),
                stream=stream,
                timeout=self.configuration.get("timeout", 30),
                params={
                    "user": self.configuration.get("user", "default"),
                    "password": self.configuration.get("password", ""),
                    "database": self.configuration["dbname"],
                },
                verify=verify,
            )
            if r.status_code != 200:
                raise Exception(r.text)
        except requests.RequestException as e:
            if e.response:
                details = "({}, Status Code: {})".format(
                    e.__class__.__name__, e.response.status_code
                )
            else:
                details = "({})".format(e.__class__.__name__)
            raise Exception("Connection error to: {} {}.".format(url, details))

    def _clickhouse_query(self, query):
        self._send_query(query)
        return {"columns": [], "rows": []}

register(WriteableClickHouse)
