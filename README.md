# To-Do List App

A simple to-do list: add tasks, check them off, drag them to reorder, delete them.

- **Backend:** Python + FastAPI (`backend/main.py`)
- **Frontend:** React + Vite (`frontend/src/App.jsx`)
- **Database:** SQLite, a SQL database stored in one file, `backend/todos.db`, created automatically

## What you need installed (one time)

1. **Python 3.10 or newer**: https://www.python.org/downloads/
   (On Windows, tick "Add Python to PATH" during install.)
2. **Node.js 20 or newer** (LTS version): https://nodejs.org/

Check they work by opening a terminal and running:

```
python --version
node --version
```

(On Mac/Linux use `python3` instead of `python` everywhere below.)

## First-time setup

Open a terminal in the `todo-app` folder and run:

**Mac / Linux**
```
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ../frontend
npm install
npm run build
cd ..
```

**Windows (PowerShell)**
```
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ..\frontend
npm install
npm run build
cd ..
```

## Run the app

```
cd backend
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
uvicorn main:app --port 8000
```

Now open **http://localhost:8000** in your browser. Press `Ctrl+C` in the
terminal to stop the server. Your tasks are saved in `backend/todos.db`.

Bonus: http://localhost:8000/docs shows an interactive page listing every API endpoint.

## Making changes (development mode)

If you want to edit the code and see changes instantly, use two terminals:

- Terminal 1: `cd backend`, activate the venv, then `uvicorn main:app --reload --port 8000`
- Terminal 2: `cd frontend`, then `npm run dev`

Then open **http://localhost:5173**. The page reloads automatically when you save a file.
When you're done, run `npm run build` again so the version on port 8000 is up to date.

## API endpoints

| Method | Path                  | What it does                               |
|--------|-----------------------|--------------------------------------------|
| GET    | /api/todos            | List all tasks, in order                   |
| POST   | /api/todos            | Add a task `{"title": "..."}`              |
| PATCH  | /api/todos/{id}       | Update `{"title": ...}` / `{"done": true}` |
| DELETE | /api/todos/{id}       | Delete a task                              |
| PUT    | /api/todos/reorder    | Save a new order `{"ids": [3,1,2]}`        |
