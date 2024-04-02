from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from base import Base

class EventLogs(Base):
    """ Event Logs """

    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True)
    message = Column(String(250), nullable=False)
    message_code = Column(String(10), nullable=False)
    code_0001 = Column(Integer, nullable=False)
    code_0002 = Column(Integer, nullable=False)
    code_0003 = Column(Integer, nullable=False)
    code_0004 = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, message, message_code, code_0001, code_0002, code_0003, code_0004):
        self.message = message
        self.message_code = message_code
        self.code_0001 = code_0001
        self.code_0002 = code_0002
        self.code_0003 = code_0003
        self.code_0004 = code_0004
        self.date_created = datetime.now()

    def to_dict(self):
        dict = {}

        dict['id'] = self.id
        dict['message'] = self.message
        dict['message_code'] = self.message_code
        dict['0001'] = self.code_0001
        dict['0002'] = self.code_0002
        dict['0003'] = self.code_0003
        dict['0004'] = self.code_0004
        dict['date_created'] = self.date_created

        return dict
