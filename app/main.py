from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import user_router, waste_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router.router)
app.include_router(waste_router.router)