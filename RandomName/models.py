from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Members(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    team = Column(String)
    hosted = Column(Boolean, default=False)
    exception = Column(String, default="No")
