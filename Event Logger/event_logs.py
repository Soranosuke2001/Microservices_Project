from sqlalchemy import Column, Integer, String, DateTime
from base import Base
from datetime import datetime

class EventLogs(Base):
    """ Event Logs """

    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True)
    message = Column(String(250), nullable=False)
    message_code = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, message, message_code):
        self.message = message
        self.message_code = message_code
        self.date_created = datetime.now()

    def to_dict(self):
        dict = {}

        dict['id'] = self.id
        dict['message'] = self.message
        dict['message_code'] = self.message_code
        dict['date_created'] = self.date_created

        return dict