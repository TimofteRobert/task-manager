from fastapi import FastAPI

from app.database import Base, engine

app = FastAPI(title="Task Manager API")
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Task Manager API"}
