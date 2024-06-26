from typing import Optional
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
import auth, user, symptom
from fastapi import Request
import logging

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(symptom.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    logging.info(body.decode())
    response = await call_next(request)
    return response



origins = [
    "http://localhost:8081",  # Adjust the port if your frontend runs on a different one
    "http://127.0.0.1:8081",  # Adjust the port if your frontend runs on a different one
    "https://yourfrontenddomain.com",
    "http://192.168.50.207"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins from the list
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

logging.basicConfig(level=logging.INFO)