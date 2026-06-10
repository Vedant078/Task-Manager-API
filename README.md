# Task Manager API

A RESTful API for managing tasks, built with **FastAPI**, **SQLModel**, and **PostgreSQL**.

---

## Tech Stack

- **FastAPI** — web framework
- **SQLModel** — ORM + schema validation
- **PostgreSQL** — database
- **Pydantic** — request/response validation
- **Uvicorn** — ASGI server

---

## Project Structure

```
API_project/
├── task_api_project.py   # main app, all route handlers
├── database.py           # engine, session, db init
├── models.py             # Task table model
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vedant078/Task-Manager-API.git
cd Task-Manager-API
```

### 2. Install dependencies

```bash
pip install fastapi sqlmodel psycopg2-binary uvicorn
```

### 3. Create the PostgreSQL database

```bash
psql -U postgres
CREATE DATABASE task_db;
\q
```

> The app connects to `postgresql://localhost/task_db` by default (`database.py`).  
> Tables are auto-created on startup via `SQLModel.metadata.create_all()`.

### 4. Run the server

```bash
uvicorn task_api_project:app --reload
```

Server runs at: `http://127.0.0.1:8000`

---

## Data Model

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | int | auto-generated primary key |
| `descp` | str | max 30 characters |
| `priority` | str | `Low` / `Medium` / `High` |
| `status` | str | `To-do` / `In-progress` / `Done` |

---

## API Endpoints

### `GET /`
Health check / welcome message.

**Response:**
```json
{
  "message": "WELCOME to Task API",
  "developer": "Vedant Limbasiya",
  "timestamp": "..."
}
```

---

### `GET /task/get-tasks`
Fetch all tasks. Optionally filter by priority.

**Query param:** `priority` (optional) — `Low`, `Medium`, `High`

```
GET /task/get-tasks
GET /task/get-tasks?priority=High
```

---

### `GET /task/get-task/{task_id}`
Fetch a single task by ID.

```
GET /task/get-task/1
```

Returns `404` if task not found.

---

### `POST /task/create-task`
Create a new task.

**Request body:**
```json
{
  "descp": "Reading",
  "priority": "High",
  "status": "In-progress"
}
```

> `priority` defaults to `Medium`, `status` defaults to `To-do` if omitted.

---

### `PATCH /task/update-task/{task_id}`
Partially update an existing task. Only send fields you want to change.

```
PATCH /task/update-task/1
```

**Request body:**
```json
{
  "descp": "Swimming"
}
```

Returns `404` if task not found.

---

### `DELETE /task/delete-task/{task_id}`
Delete a task by ID.

```
DELETE /task/delete-task/1
```

**Response:**
```json
{
  "message": "Task 1 deleted successfully"
}
```

Returns `404` if task not found.

---

### `GET /task/filter/{task_status}`  *(via get-tasks query param)*
Filter tasks by status.

```
GET /task/get-tasks   (extend with status filter if needed)
```

> Currently status filtering is handled through the `get-tasks` endpoint with priority filter. Status filter can be added similarly.

---

## Testing with Postman

Set a Postman environment variable:

| Variable | Value |
|----------|-------|
| `baseURL` | `http://127.0.0.1:8000` |

Then use `{{baseURL}}/task/get-tasks`, `{{baseURL}}/task/create-task`, etc.

---

## Developer

**Vedant Limbasiya** — [GitHub](https://github.com/Vedant078)