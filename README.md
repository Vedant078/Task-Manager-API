
# Task Management REST API Documentation

This documentation provides a precise overview of the Task Management REST API endpoints and configurations based on the project's Postman schema.

---

## Environment Configuration

Set the global variable in Postman to map the deployment environment:
* **`{{baseURL}}`**: `http://127.0.0.1:8000`

---

## API Endpoints Specification

### 1. Welcome Page
* **Method:** GET
* **URL:** `{{baseURL}}/`
* **Description:** Service root index acting as an operational heartbeat check.

### 2. Get All Tasks
* **Method:** GET
* **URL:** `{{baseURL}}/task/get-tasks`
* **Description:** Retrieves the global dictionary containing all active task records. 
* **Note:** Do not add a trailing slash to the path.

### 3. Create Task
* **Method:** POST
* **URL:** `{{baseURL}}/task/create-task?task_id=18`
* **Query Parameter:** `task_id` (Required)
* **Body (JSON):**
```json
{
    "descp": "Reading",
    "priority": "High",
    "status": "In-progress"
}

```

* **Description:** Enforces schema validation using Pydantic models and provisions a new task database record.

### 4. Get Specific Task

* **Method:** GET
* **URL:** `{{baseURL}}/task/get-task/32`
* **Path Parameter:** `task_id`
* **Description:** Fetches explicit details for a single target item. Raises an HTTP 404 error if the ID does not exist.

### 5. Update Task

* **Method:** PATCH
* **URL:** `{{baseURL}}/task/update-task/1`
* **Path Parameter:** `task_id`
* **Body (JSON):**

```json
{
    "descp": "swimming"
}

```

* **Description:** Executes runtime-safe partial mutations on existing keys via `.model_dump(exclude_unset=True)`. Unspecified payload fields are left unaltered.

### 6. Delete Task

* **Method:** DELETE
* **URL:** `{{baseURL}}/task/delete-task/32`
* **Path Parameter:** `task_id`
* **Expected Response (JSON):**

```json
{
    "message": "Task 32 deleted successfully"
}

```

* **Description:** Permanently unsets and clears the designated target task from the active database memory.

### 7. Filter Tasks by Status

* **Method:** GET
* **URL:** `{{baseURL}}/task/filter/To-do`
* **Path Parameter:** `task_status` (Options: `To-do`, `In-progress`, `Done`)
* **Description:** Evaluates the active database indices and compiles a response containing only tasks matching the queried state.


