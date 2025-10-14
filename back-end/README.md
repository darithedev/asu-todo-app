# ASU Todo App – Backend (FastAPI)

## Overview
FastAPI service providing authentication, user management, tasks, and labels APIs backed by MongoDB via Beanie ODM.

## Tech Stack
- FastAPI, Uvicorn
- Beanie (MongoDB ODM), Pydantic
- Auth: OAuth2 (password), JWT (`python-jose`), Passlib (bcrypt)
- Python 3.13

## Requirements
- Python 3.13
- MongoDB running locally or remotely

## Environment Variables
Create `.env` from `example.env` and set:
- `MONGODB_URI=mongodb://localhost:27017/asu_todo`
- `SECRET_KEY=your-secret-key`
- `ACCESS_TOKEN_EXPIRE_MINUTES=30`

## Setup & Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server (from `back-end/`):
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. API: `http://localhost:8000`
   Docs: `http://localhost:8000/docs`

## Project Structure
```
back-end/
  app/
    main.py        # FastAPI initialization, routers
    database.py    # MongoDB/Beanie init
    routes/        # auth, users, tasks, labels
    models/        # User, Task, Label schemas & documents
  requirements.txt
```

## Key Endpoints (Summary)
- Auth
  - POST `/auth/register` – create user
  - POST `/auth/login` – OAuth2 password login (form fields: username, password)
  - GET `/auth/me` – current user info (Bearer token)
  - POST `/auth/logout` – invalidate refresh token
  - POST `/auth/refresh` – rotate access token
- Users
  - GET `/users/` – list (admin only if applicable)
  - GET `/users/{id}` – details
- Tasks (Bearer token required)
  - GET `/tasks/user/{user_id}` – list tasks for user
  - POST `/tasks/` – create task (title, description?, priority, deadline, label_ids[])
  - PATCH `/tasks/{task_id}` – partial update any fields
  - DELETE `/tasks/{task_id}` – delete
  - PUT `/tasks/{task_id}/labels` – replace labels on a task
  - POST `/tasks/{task_id}/labels/{label_id}` – add one label
  - DELETE `/tasks/{task_id}/labels/{label_id}` – remove one label
- Labels (Bearer token required)
  - GET `/labels/` – list labels for current user
  - POST `/labels/` – create label (name, color?, description?)
  - PATCH `/labels/{label_id}` – update label
  - DELETE `/labels/{label_id}` – delete label

## Data Models (Highlights)
- User
  - `email`, `username`, `hashed_password`, optional profile fields
- Task
  - `title` (required), `description?`, `priority` (High/Medium/Low), `deadline` (datetime), `status`, `label_ids[]`, `user_id`
- Label
  - `name` (required), `color?`, `description?`, `user_id`

## Development Notes
- Ensure MongoDB is reachable via `MONGODB_URI`.
- Use `/docs` to explore and test endpoints.
- Passwords are hashed with bcrypt; JWT tokens are signed with `SECRET_KEY`.

