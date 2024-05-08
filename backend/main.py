from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from models import User, SymptomEpisode
from database import SessionLocal, engine
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:8081",  # Adjust the port if your frontend runs on a different one
    "https://yourfrontenddomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins from the list
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Your JWT secret and algorithm
SECRET_KEY = "test-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserCreate(BaseModel):
    username: str
    email: str
    name: str
    password: str

class SymptomCreate(BaseModel):
    date: datetime
    severity: int
    notes: str
    mood: str
    weather: str

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return "complete"

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")
    
def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if verify_token(token=token):
        payload = verify_token(token=token)
        username: str = payload.get("sub")
        return get_user_by_username(db, username)
    else:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")

@app.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}

#testing purposes only
@app.get("/verify-token-payload/{token}")
async def verify_user_token(token: str):
    payload = verify_token(token=token)
    return payload

@app.post("/create-symptom-episode/{token}")
def create_symptom_episode(token: str, symptom_episode: SymptomCreate, db: Session = Depends(get_db)):
    user = get_current_user_from_token(token=token, db=db)
    if user:
        db_symptom_episode = SymptomEpisode(user_id=user.id, 
                                            date=symptom_episode.date, 
                                            severity=symptom_episode.severity, 
                                            notes=symptom_episode.notes, 
                                            mood=symptom_episode.mood, 
                                            weather=symptom_episode.weather)
        db.add(db_symptom_episode)
        db.commit()
        return {"message": "Symptom episode created successfully"}
    else:
        return {"message": "User not found"}
    
@app.get("/all-symptom-episodes/{token}")
def get_symptom_episodes(token: str, db: Session = Depends(get_db)):
    user = get_current_user_from_token(token=token, db=db)
    if user:
        symptom_episodes = db.query(SymptomEpisode).join(User).filter(User.username == user.username).all()
        return {"symptom_episodes": symptom_episodes}
    else:
        return {"message": "User not found"}

    

@app.delete("/delete-symptom-episode/{token}/{id}")
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
