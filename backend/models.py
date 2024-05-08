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
    episodes = relationship("SymptomEpisode", back_populates="user")

class SymptomEpisode(Base):
    __tablename__ = "symptom_episodes"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    severity = Column(Integer)
    notes = Column(String)
    mood = Column(String)
    weather = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="episodes")

# Create the database tables if they don't exist

Base.metadata.create_all(bind=engine)
