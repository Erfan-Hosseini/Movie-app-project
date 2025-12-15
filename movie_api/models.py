from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class UserDB(Base):
    __tablename__ = "users"

    # Standard columns
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, index=True, unique=True)
    hashed_password = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    time_created = Column(DateTime, default=datetime.utcnow)


    movies = relationship("MovieDB", back_populates="owner")


class MovieDB(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    director = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    available = Column(Boolean, default=True)


    owner_id = Column(Integer, ForeignKey("users.id"))


    owner = relationship("UserDB", back_populates="movies")



