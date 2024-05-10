# symptom.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SymptomEpisode, User, SymptomCreate
from database import get_db
from auth import get_current_user_from_token

router = APIRouter()

@router.post("/create-symptom-episode/{token}")
def create_symptom_episode(token: str, symptom_episode: SymptomCreate, db: Session = Depends(get_db)):
    user = get_current_user_from_token(token=token, db=db)
    if user:
        db_symptom_episode = SymptomEpisode(user_id=user.id, 
                                            date=symptom_episode.date, 
                                            severity=symptom_episode.severity, 
                                            notes=symptom_episode.notes, 
                                            mood=symptom_episode.mood, 
                                            weather=symptom_episode.weather,
                                            food_eaten=symptom_episode.food_eaten,
                                            medications_before=symptom_episode.medications_before,
                                            medications_after=symptom_episode.medications_after,
                                            activities=symptom_episode.activities,
                                            work_day=symptom_episode.work_day,
                                            sleep_rating=symptom_episode.sleep_rating)
        db.add(db_symptom_episode)
        db.commit()
        return {"message": "Symptom episode created successfully"}
    else:
        return {"message": "User not found"}

@router.get("/all-symptom-episodes/{token}")
def get_symptom_episodes(token: str, db: Session = Depends(get_db)):
    user = get_current_user_from_token(token=token, db=db)
    if user:
        symptom_episodes = db.query(SymptomEpisode).join(User).filter(User.username == user.username).all()
        return {"symptom_episodes": symptom_episodes}
    else:
        return {"message": "User not found"}

@router.delete("/delete-symptom-episode/{token}/{id}")
def delete_symptom_episode(token: str, id: int, db: Session = Depends(get_db)):
    user = get_current_user_from_token(token=token, db=db)
    if user:
        db_symptom_episode = db.query(SymptomEpisode).filter(SymptomEpisode.id == id).first()
        if user.id == db_symptom_episode.user_id:
            if not db_symptom_episode:
                raise HTTPException(status_code=404, detail="Symptom episode not found")
            db.delete(db_symptom_episode)
            db.commit()
            return {"message": "Symptom episode deleted successfully"}
        else:
            return {"message": "User not authorized to delete this symptom episode"}
    else:
        return {"message": "User not found"}

@router.put("/edit-symptom-episode/{token}/{id}")
def edit_symptom_episode(token: str, id: int, symptom_episode: SymptomCreate, db: Session = Depends(get_db)):
    user = get_current_user_from_token(token=token, db=db)
    if user:
        db_symptom_episode = db.query(SymptomEpisode).filter(SymptomEpisode.id == id).first()
        if user.id == db_symptom_episode.user_id:
            if not db_symptom_episode:
                raise HTTPException(status_code=404, detail="Symptom episode not found")
            
            db_symptom_episode.date = symptom_episode.date
            db_symptom_episode.severity = symptom_episode.severity
            db_symptom_episode.notes = symptom_episode.notes
            db_symptom_episode.mood = symptom_episode.mood
            db_symptom_episode.weather = symptom_episode.weather
            db_symptom_episode.food_eaten = symptom_episode.food_eaten
            db_symptom_episode.medications_before = symptom_episode.medications_before
            db_symptom_episode.medications_after = symptom_episode.medications_after
            db_symptom_episode.activities = symptom_episode.activities
            db_symptom_episode.work_day = symptom_episode.work_day
            db_symptom_episode.sleep_rating = symptom_episode.sleep_rating
            
            db.commit()
            return {"message": "Symptom episode updated successfully"}
        else:
            return {"message": "User not authorized to edit this symptom episode"}
    else:
        return {"message": "User not found"}