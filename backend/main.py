"""To-do list API: FastAPI + SQLAlchemy + SQLite (local) or PostgreSQL (online)."""
import os
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import Boolean, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

# --- Database setup -------------------------------------------------------
# Online, set DATABASE_URL to a PostgreSQL connection string.
# Locally, it falls back to SQLite: a single file (todos.db) next to this script.
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    # Hosting providers hand out "postgres://..." URLs; tell SQLAlchemy to use psycopg.
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    DB_PATH = Path(__file__).parent / "todos.db"
    engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    position: Mapped[int] = mapped_column(Integer, default=0)  # order in the list


Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Request / response shapes -------------------------------------------
class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


class TodoOut(BaseModel):
    id: int
    title: str
    done: bool
    position: int

    model_config = {"from_attributes": True}


class Reorder(BaseModel):
    ids: list[int]  # todo ids in their new order


# --- API ------------------------------------------------------------------
app = FastAPI(title="To-Do API")

# Allows the React dev server (port 5173) to talk to this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_todo_or_404(db: Session, todo_id: int) -> Todo:
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.get("/api/todos", response_model=list[TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return db.scalars(select(Todo).order_by(Todo.position, Todo.id)).all()


@app.post("/api/todos", response_model=TodoOut, status_code=201)
def create_todo(data: TodoCreate, db: Session = Depends(get_db)):
    title = data.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    last = db.scalar(select(func.max(Todo.position))) or 0
    todo = Todo(title=title, position=last + 1)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.patch("/api/todos/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, data: TodoUpdate, db: Session = Depends(get_db)):
    todo = get_todo_or_404(db, todo_id)
    if data.title is not None:
        if not data.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        todo.title = data.title.strip()
    if data.done is not None:
        todo.done = data.done
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db.delete(get_todo_or_404(db, todo_id))
    db.commit()


@app.put("/api/todos/reorder", response_model=list[TodoOut])
def reorder_todos(data: Reorder, db: Session = Depends(get_db)):
    for position, todo_id in enumerate(data.ids):
        get_todo_or_404(db, todo_id).position = position
    db.commit()
    return list_todos(db)


# --- Serve the built React app (after `npm run build`) --------------------
FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
