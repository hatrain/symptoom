from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base
from database import engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database import engine

#TODO: modify to include extra fields
class UserCreate(BaseModel):
    username: str
    email: str
    name: str
    password: str
    family_history: Optional[str] = None
    medications: Optional[str] = None
    phone_number: Optional[str] = None

#TODO: modify to include extra fields
class SymptomCreate(BaseModel):
    date: datetime
    severity: int
    notes: str
    mood: str
    weather: str
    food_eaten: Optional[str] = None
    medications_before: Optional[str] = None
    medications_after: Optional[str] = None
    activities: Optional[str] = None
    work_day: Optional[str] = None
    sleep_rating: Optional[int] = None

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    family_history = Column(String)  # column for family history of symptoms or conditions
    medications = Column(String)  # column for medications the user is currently taking
    phone_number = Column(String)  # column for phone number of the user
    episodes = relationship("SymptomEpisode", back_populates="user")

class SymptomEpisode(Base):
    __tablename__ = "symptom_episodes"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    severity = Column(Integer)
    notes = Column(String)
    mood = Column(String)
    weather = Column(String)
    food_eaten = Column(String)  # column for food eaten that day
    medications_before = Column(String)  # column for medications taken before the symptoms started
    medications_after = Column(String)  # column for medications taken after the symptoms started
    activities = Column(String)  # column for activities done that day
    work_day = Column(String)  # column for work day or day off
    sleep_rating = Column(Integer)  # column for the amount of sleep the user got that night; rating in integer
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="episodes")

# Create the database tables if they don't exist

Base.metadata.create_all(bind=engine)
