from sqlalchemy.orm import session
from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
from typing import List
import shutil

from app.database.database import get_db
from app.models import models
from app.schema import schema
from app.oauth.oauth2 import get_current_user_logged_in
from app.utils import auth_utils



router = APIRouter(
    prefix="/supervisor",
    tags=["Supervisor Operations"]
)

@router.post(
    "/employees",
    status_code=status.HTTP_201_CREATED,
    response_model=schema.UserResponse
)
def create_employee(
    employee: schema.UserCreate,
    db: session = Depends(get_db),
    current_user = Depends(get_current_user_logged_in)
):

    if current_user.role != "SUPERVISOR":
        raise HTTPException(
            status_code=403,
            detail="Only supervisors can create employees"
        )

    hashed_password = auth_utils.get_hashed_password(employee.password)

    new_employee = models.Users(
        username=employee.username,
        full_name=employee.full_name,
        password=hashed_password,
        role="EMPLOYEE"
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee

@router.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=schema.TaskResponse)
def create_task(
    task: schema.TaskCreate,
    db: session = Depends(get_db),
    current_user = Depends(get_current_user_logged_in)
):

    if current_user.role != "SUPERVISOR":
        raise HTTPException(status_code=403, detail="Only supervisors can create tasks")

    new_task = models.Tasks(
        title=task.title,
        description=task.description,
        assigned_to=task.assigned_to,
        created_by=current_user.user_id,
        status="ASSIGNED"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.post("/tasks/{task_id}/files", status_code=status.HTTP_201_CREATED)
def upload_task_file(task_id: int,file: UploadFile = File(...),db: session = Depends(get_db),current_user = Depends(get_current_user_logged_in)):

    if current_user.role != "SUPERVISOR":
        raise HTTPException(status_code=403)

    task = db.query(models.Tasks).filter(models.Tasks.task_id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = models.TaskFiles(
        task_id=task_id,
        filename=file.filename,
        filepath=file_path,
        uploaded_by=current_user.user_id
    )

    db.add(new_file)
    db.commit()

    return {"message": "file uploaded"}


@router.get("/tasks/review", response_model=List[schema.TaskResponse])
def review_tasks(db: session = Depends(get_db),current_user = Depends(get_current_user_logged_in)):

    if current_user.role != "SUPERVISOR":
        raise HTTPException(status_code=403)

    tasks = db.query(models.Tasks).filter(
        models.Tasks.status == "RESOLVED"
    ).all()

    return tasks


@router.patch("/tasks/{task_id}/close", response_model=schema.TaskResponse)
def close_task(task_id: int,db: session = Depends(get_db),current_user = Depends(get_current_user_logged_in)):

    if current_user.role != "SUPERVISOR":
        raise HTTPException(status_code=403)

    task = db.query(models.Tasks).filter(
        models.Tasks.task_id == task_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != "RESOLVED":
        raise HTTPException(status_code=400, detail="Task must be resolved first")

    task.status = "DONE"

    db.commit()
    db.refresh(task)

    return task