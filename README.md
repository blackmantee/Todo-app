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

## Publishing it on the internet

The app is packaged with a `Dockerfile`, so hosting services know how to build and run it.
We use **Render** to run the app and **Neon** for a free PostgreSQL database.
(Render's free servers erase their disk on restart, so SQLite would lose your tasks there.)

1. **Put the code on GitHub.** Create a free account at github.com and a new repository, then push this folder to it.
2. **Create the database.** Sign up at neon.tech, create a project, and copy its
   **connection string**. It looks like `postgresql://user:password@host/dbname?sslmode=require`.
   Treat it like a password.
3. **Create the web service.** Sign up at render.com with your GitHub account, click
   **New → Web Service**, and pick your repository. Render sees the `Dockerfile` automatically.
   Choose the **Free** instance type.
4. Under **Environment Variables**, add `DATABASE_URL` and paste the Neon connection string as its value.
5. Click **Create Web Service**. After a few minutes you get a link like
   `https://your-app.onrender.com`. That's your live to-do list.

Every time you push new code to GitHub, Render rebuilds and republishes automatically.

Note: free Render services go to sleep when unused, so the first visit after a while can take up to about a minute to load.
Also note that anyone with the link can see and edit the list, because the app has no login.
