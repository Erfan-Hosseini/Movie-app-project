from fastapi import FastAPI
from .database import Base, engine
from .routers import users, movies
from .security import get_current_user
from . import models

app = FastAPI()
app.include_router(users.router)
app.include_router(movies.router)


Base.metadata.create_all(bind=engine)


    


