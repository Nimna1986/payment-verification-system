from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

from app.database.dependencies import get_db

from app.database.connection import engine
from app.database.base import Base

import app.models  # Import models to register them with SQLAlchemy
from app.routers.users import router as users_router
from app.routers.payments import router as payments_router
from app.routers.orders import router as orders_router


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(payments_router)
app.include_router(orders_router)

