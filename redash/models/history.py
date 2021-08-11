from sqlalchemy_utils.models import generic_repr
from .base import db, Column, primary_key, key_type
import datetime
import logging

@generic_repr("id", "query_string", "executed_at")
class UserHistory(db.Model):
    id = primary_key("UserHistory")
    query_string = Column(db.Text)
    user_id = Column(key_type("User"), db.ForeignKey("users.id"))
    executed_at = Column(db.DateTime(True), default=db.func.now())

    __tablename__ = "UserHistory"

    def to_dict(self):
        return {"query_string": self.query_string, "executed_at": int(datetime.datetime.timestamp(self.executed_at))}
    
    @classmethod
    def get_history(cls, user_id):
        return (
            cls.query.filter(
                cls.user_id == user_id
            )
            .order_by(cls.executed_at.desc())
        )
        
        
    @classmethod
    def delete_old_user_history(cls):
        delete_from = datetime.datetime.now() - datetime.timedelta(days=7)
        logging.info("Deleting UserHistory items older then {}".format(delete_from))
        deleted = cls.query.filter(cls.executed_at < delete_from).delete(synchronize_session=False)
        db.session.commit()
        logging.info("Number of deleted UserHistory items: {}".format(deleted))
        