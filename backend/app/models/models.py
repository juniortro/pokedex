from sqlalchemy import Column, Integer, String
from ..database.database import Base

class Pokemon(Base):
    __tablename__ = "pokemon"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)