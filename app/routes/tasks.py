from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project, Task
from app.schemas import TaskCreate, TaskRead

router = APIRouter(prefix="/projects/{project_id}/tasks", tags={"tasks"})


# Helper function in case of 404
def get_project_or_404(project_id: int, db: Session) -> Project:
    db_project = db.get(Project, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.post("", response_model=TaskRead, status_code=201)
def create_task(project_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_project = get_project_or_404(project_id, db)
    db_task = Task(**task.model_dump(), project=db_project)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("", response_model=list[TaskRead])
def list_tasks(project_id: int, db: Session = Depends(get_db)):
    get_project_or_404(project_id, db)
    return db.query(Task).filter(Task.project_id == project_id).all()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(project_id: int, task_id: int, db: Session = Depends(get_db)):
    get_project_or_404(project_id, db)
    db_task = db.get(Task, task_id)
    if db_task is None or db_task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(project_id: int, task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    get_project_or_404(project_id, db)
    db_task = db.get(Task, task_id)
    if db_task is None or db_task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task.model_dump().items():
        setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)
        return db_task


@router.delete("/{task_id}", status_code=204)
def delete_task(project_id: int, task_id: int, db: Session = Depends(get_db)):
    get_project_or_404(project_id, db)
    db_task = db.get(Task, task_id)
    if db_task is None or db_task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
