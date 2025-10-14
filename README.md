# ASU Todo App

## Overview
ASU Todo App is a full‑stack task management application that lets users register, sign in, and manage their personal task lists with priorities, deadlines, and labels. The app is built with a FastAPI backend (MongoDB persistence) and a Next.js + Tailwind CSS frontend.

## Tech Stack
- Backend: FastAPI, Beanie (ODM), MongoDB, Pydantic, Python 3.13
- Auth: OAuth2 (password), JWT via `python-jose`, Passlib (bcrypt)
- Frontend: Next.js (React), Tailwind CSS, Axios
- Runtime/Dev: Uvicorn, Node.js/npm

## Project Structure
```
asu-todo-app/
  back-end/                 # FastAPI service
  front-end/                # Next.js app
  README.md                 # This file
```

## Prerequisites
- Python 3.13
- Node.js 18+ and npm
- A running MongoDB instance (local or remote)

## Environment Variables
Copy example env files and adjust as needed:

Backend (back-end/example.env → back-end/.env):
- `MONGODB_URI=mongodb://localhost:27017/`
- `SECRET_KEY=your-secret-key`
- `ACCESS_TOKEN_EXPIRE_MINUTES=30`

Frontend (front-end/example.env → front-end/.env):
- `NEXT_PUBLIC_API_URL=http://localhost:8000`

## Running the Backend
1. Open a terminal in `back-end/`
2. (Optional) Create/activate a venv
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set environment variables (copy example.env → .env)
5. Start FastAPI with Uvicorn:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
6. API should be available at `http://localhost:8000` and docs at `http://localhost:8000/docs`.

## Running the Frontend
1. Open another terminal in `front-end/`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Copy example.env → .env and ensure `NEXT_PUBLIC_API_URL` points to the backend (default `http://localhost:8000`).
4. Start the dev server:
   ```bash
   npm run dev
   ```
5. Open `http://localhost:3000` in the browser.

## Completed Features
- User Management
  - User registration with validation
  - Login with JWT and protected routes
  - Secure logout
- Task Management
  - Create, view, update, delete tasks
  - Required fields: title, optional description, priority (High/Medium/Low), deadline
  - Toggle completion status
  - Only the owner sees and mutates their tasks
- Labels
  - Create/manage user labels (name, color)
  - Assign multiple labels to tasks
  - Filter tasks by selected labels
- Persistence
  - Users, tasks, labels stored in MongoDB via Beanie ODM

## Stretch Goals (Optional / Future Work)
- Additional task filters (status, priority) and sorting
- Task search by title/description
- Pagination and infinite scrolling
- Label statistics and task analytics
- Role-based admin operations and audit logs

## Scripts (Frontend)
- `npm run dev` – start Next.js dev server
- `npm run build` – build production bundle
- `npm run start` – run production build
- `npm run lint` – lint the project

## Notes
- If you see a white screen during development, try clearing `.next/` and restarting `npm run dev`.
- Ensure the frontend `.env` has `NEXT_PUBLIC_API_URL` set and the backend is running.
