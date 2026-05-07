# Task Management System (FastAPI)

A simple role-based task management system built with FastAPI, PostgreSQL, and SQLAlchemy.  
The system supports supervisors and employees with controlled task workflows, file uploads, and task history tracking.

---

## Features

### Supervisor
- Login
- Create employees
- Create and assign tasks
- Upload supporting files
- Review completed tasks
- Mark tasks as DONE

### Employee
- Login
- View assigned tasks
- View task files
- Update task progress
- Mark tasks as completed (for review)

---

## Authentication & Roles

The system uses JWT authentication.

### Roles:
- `SUPERVISOR`
- `EMPLOYEE`

Access is controlled using role-based permissions.

---

## Task Workflow

Tasks move through a controlled lifecycle:



## Running the Project with Docker

This project uses Docker Compose to run both the FastAPI backend and PostgreSQL database.

---

### 1. Prerequisites

Make sure you have:

- Docker installed → https://www.docker.com/
- Docker Compose installed (usually comes with Docker Desktop)

---

### 2. Environment Setup

Your `docker-compose.yml` already includes all required environment variables:

- Database host: `postgres`
- Database name: `emtech-db`
- Username: `emtech`
- Password: `emtech1234`
- Secret key for JWT authentication

No additional `.env` file is required unless you want to override values.

---

### 3. Build and Start Services

Run the following command in the project root:

```bash
docker-compose up --build


