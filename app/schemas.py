from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Project
class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    created_at: datetime
    tasks: list["TaskRead"] = []


# Task
class TaskCreate(BaseModel):
    title: str
    done: bool = False


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    done: bool
    created_at: datetime
    project_id: int


ProjectRead.model_rebuild()
