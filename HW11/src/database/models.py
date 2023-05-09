from sqlalchemy import Column, Integer, String, DateTime, func, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone_number = Column(String, nullable=False, unique=True, index=True)
    birthday = Column(Date, nullable=False, index=True)
    other_data = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
