from fastapi import FastAPI

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db

app = FastAPI(
    title="ShortLink API",
    description="URL Shortening Service",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message" : "Welcome to ShortLink API",
        "status" : "running"
    }

@app.get("/health/live", tags=["Health"])
def health_check():
    return {
        "status": "OK",
    }

@app.get("/health/ready", tags=["Health"])
def readiness_check(db=Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable",
        )