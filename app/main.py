from fastapi import FastAPI, Depends, HTTPException,Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.auth import register_user, login_user, refresh_access_token
from app.database.database import get_db
from app.schemas.schemas import UserCreate, TaskCreate, TaskBase, LoginData
from app.database.crud import create_task, get_tasks, update_task, delete_task, get_task
from typing import List, Optional
from app.auth.auth  import get_current_user
from app.database.database import init_db

app = FastAPI()


@app.post("/auth/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user(db, user)


@app.post("/auth/login")
async def login(
    username: str = Form(...), 
    password: str = Form(...), 
    db: AsyncSession = Depends(get_db)
):
    return await login_user(db, username, password)


@app.post("/auth/refresh")
async def refresh_token(refresh_token: str):
    return refresh_access_token(refresh_token)


@app.post("/tasks", response_model=TaskBase)
async def create_new_task(task: TaskCreate, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    return await create_task(db, task, user_id)


@app.get("/tasks", response_model=List[TaskBase])
async def read_tasks(status: Optional[str] = None, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    return await get_tasks(db, user_id, status)


@app.get("/tasks/{task_id}", response_model=TaskBase)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    task = await get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskBase)
async def update_existing_task(task_id: int, task: TaskBase, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    updated_task = await update_task(db, task_id, task, user_id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@app.delete("/tasks/{task_id}")
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    task = await get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await delete_task(db, task_id, user_id)
    return {"detail": "Task deleted successfully"}


@app.on_event("startup")
async def on_startup():
    await init_db()