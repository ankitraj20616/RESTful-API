from fastapi import FastAPI
from dependency.database import engine
from schema import user
from routers import employees


app = FastAPI()

user.Base.metadata.create_all(bind = engine)

app.include_router(employees.router)