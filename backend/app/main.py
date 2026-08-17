from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.database.connection import engine
from app.database.base import Base

import app.models  # Import models to register them with SQLAlchemy
from app.routers.users import router as users_router
from app.routers.payments import router as payments_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(payments_router)

