from sqlalchemy.orm import session
from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
from typing import List
import shutil

from app.database.database import get_db
from app.models import models
from app.schema import schema
from app.oauth.oauth2 import get_current_user_logged_in

router = APIRouter(
    prefix="/employee",
    tags=["Employee Tasks"]
)

@router.get("/tasks", response_model=List[schema.TaskResponse])
def get_my_tasks(db: session = Depends(get_db),current_user = Depends(get_current_user_logged_in)):
    if current_user.role != "EMPLOYEE":
        raise HTTPException(403, "Only employees allowed")

    tasks = db.query(models.Tasks).filter(
        models.Tasks.assigned_to == current_user.user_id
    ).all()

    return tasks

@router.get("/tasks/{task_id}", response_model=schema.TaskResponse)
def get_task(task_id: int,db: session = Depends(get_db),current_user = Depends(get_current_user_logged_in)):
    task = db.query(models.Tasks).filter(
        models.Tasks.task_id == task_id,
        models.Tasks.assigned_to == current_user.user_id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    return task


@router.put("/tasks/{task_id}/progress")
def update_progress(task_id: int,db: session = Depends(get_db),current_user = Depends(get_current_user_logged_in)):
    task = db.query(models.Tasks).filter(
        models.Tasks.task_id == task_id,
        models.Tasks.assigned_to == current_user.user_id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    old_status = task.status

    if task.status == "ASSIGNED":
        task.status = "IN_PROGRESS"

    elif task.status == "IN_PROGRESS":
        task.status = "RESOLVED"

    else:
        raise HTTPException(
            400,
            "Invalid status transition"
        )

    history = models.TaskHistory(
        task_id=task.task_id,
        old_status=old_status,
        new_status=task.status,
        changed_by=current_user.user_id,
        comment="Status updated by employee"
    )

    db.add(history)
    db.commit()
    db.refresh(task)

    return task


@router.put("/tasks/{task_id}/complete")
def mark_completed(task_id: int,db: session = Depends(get_db),current_user = Depends(get_current_user_logged_in)):
    task = db.query(models.Tasks).filter(
        models.Tasks.task_id == task_id,
        models.Tasks.assigned_to == current_user.user_id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    if task.status != "RESOLVED":
        raise HTTPException(
            400,
            "Task must be resolved first"
        )

    old_status = task.status
    task.status = "COMPLETED"

    history = models.TaskHistory(
        task_id=task.task_id,
        old_status=old_status,
        new_status="COMPLETED",
        changed_by=current_user.user_id,
        comment="Marked as completed by employee"
    )

    db.add(history)
    db.commit()

    return task


@router.get("/tasks/{task_id}/files", response_model=List[schema.TaskFileResponse])
def get_task_files(
    task_id: int,
    db: session = Depends(get_db),
    current_user = Depends(get_current_user_logged_in)
):
    task = db.query(models.Tasks).filter(
        models.Tasks.task_id == task_id,
        models.Tasks.assigned_to == current_user.user_id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    return task.files