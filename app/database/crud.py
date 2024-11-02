from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models.models import Task
from app.schemas.schemas import TaskCreate, TaskBase
from typing import Optional, List

async def create_task(db: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
    task = Task(**task_data.dict(), user_id=user_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_tasks(db: AsyncSession, user_id: int, status: Optional[str] = None) -> List[Task]:
    query = select(Task).where(Task.user_id == user_id)
    if status:
        query = query.where(Task.status == status)
    result = await db.execute(query)
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: int, task_data: TaskBase, user_id: int) -> Optional[Task]:
    query = update(Task).where(Task.id == task_id, Task.user_id == user_id).values(
        title=task_data.title, 
        description=task_data.description, 
        status=task_data.status
    ).execution_options(synchronize_session="fetch")
    await db.execute(query)
    await db.commit()
    return await get_task(db, task_id, user_id)

async def get_task(db: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> None:
    query = delete(Task).where(Task.id == task_id, Task.user_id == user_id)
    await db.execute(query)
    await db.commit()
