from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    TIMESTAMP,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.database.database import Base


class Users(Base):
    """
    System users
    """

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    # SUPERVISOR / EMPLOYEE
    role = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    assigned_tasks = relationship("Tasks", foreign_keys="Tasks.assigned_to",back_populates="employee")
    created_tasks = relationship("Tasks",foreign_keys="Tasks.created_by",back_populates="supervisor")


class Tasks(Base):
    """
    Tasks table
    """

    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String,nullable=False,server_default="CREATED")  # CREATED / ASSIGNED / IN_PROGRESS / RESOLVED / DONE
    assigned_to = Column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"),nullable=False)
    created_by = Column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"),onupdate=text("now()"))
    employee = relationship("Users",foreign_keys=[assigned_to],back_populates="assigned_tasks")
    supervisor = relationship("Users",foreign_keys=[created_by],back_populates="created_tasks")
    files = relationship("TaskFiles",back_populates="task",cascade="all, delete")
    history = relationship("TaskHistory",back_populates="task",cascade="all, delete")


class TaskFiles(Base):
    """
    Uploaded files for tasks
    """

    __tablename__ = "task_files"

    file_id = Column(Integer, primary_key=True, nullable=False)
    task_id = Column(Integer,ForeignKey("tasks.task_id", ondelete="CASCADE"),nullable=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    uploaded_by = Column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    task = relationship("Tasks",back_populates="files")


class TaskHistory(Base):
    """
    Tracks task status changes
    """

    __tablename__ = "task_history"

    history_id = Column(Integer, primary_key=True, nullable=False)
    task_id = Column(Integer,ForeignKey("tasks.task_id", ondelete="CASCADE"),nullable=False)
    old_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    comment = Column(Text)
    changed_by = Column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"),nullable=False)
    changed_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    task = relationship("Tasks",back_populates="history")







# class Notifications(Base):
#     """
#     User notifications
#     """

#     __tablename__ = "notifications"

#     notification_id = Column(Integer, primary_key=True, nullable=False)
#     user_id = Column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"),nullable=False)
#     message = Column(Text, nullable=False)
#     # is_read = Column(
#     #     String,
#     #     nullable=False,
#     #     server_default="false"
#     # )

#     created_at = Column(
#         TIMESTAMP(timezone=True),
#         nullable=False,
#         server_default=text("now()")
#     )