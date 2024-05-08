from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base
from database import engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database import Base
from database import engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    family_history = Column(String)  # column for family history of symptoms or conditions
    medications = Column(String)  # column for medications the user is currently taking
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
