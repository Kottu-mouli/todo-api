# Todo REST API

Production-oriented Django REST Framework Todo API using:

- Django 4.2.5
- Django REST Framework 3.14.0
- SimpleJWT 5.3.1
- PostgreSQL in production / SQLite locally
- Gunicorn
- django-cors-headers

## Setup

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `SECRET_KEY`.

Then:

```bash
python manage.py migrate
python manage.py runserver
```

API base URL:

```text
http://127.0.0.1:8000/api/
```

## Authentication

Register:

```http
POST /api/users/register/
```

```json
{
  "username": "mouli",
  "email": "mouli@example.com",
  "first_name": "Mouli",
  "last_name": "Sai",
  "password": "StrongPassword123"
}
```

Obtain tokens:

```http
POST /api/token/
```

```json
{
  "username": "mouli",
  "password": "StrongPassword123"
}
```

Use the access token:

```http
Authorization: Bearer <access_token>
```

Refresh:

```http
POST /api/token/refresh/
```

```json
{
  "refresh": "<refresh_token>"
}
```

## Todo endpoints

```text
GET    /api/todos/
POST   /api/todos/
GET    /api/todos/{id}/
PUT    /api/todos/{id}/
PATCH  /api/todos/{id}/
DELETE /api/todos/{id}/

POST   /api/todos/{id}/complete/
POST   /api/todos/{id}/reopen/

GET    /api/todos/stats/
GET    /api/todos/by-status/?status=pending
GET    /api/todos/by-status/?status=in_progress
GET    /api/todos/by-status/?status=completed

GET    /api/users/me/
```

Every Todo query is filtered by the authenticated user, so one user cannot retrieve another user's todos by changing an ID.

## Production notes

Set a strong `SECRET_KEY`, `DEBUG=False`, real `ALLOWED_HOSTS`, PostgreSQL `DATABASE_URL`, and production CORS origins on Render.

The Render start command runs migrations before Gunicorn. The same behavior is represented in the `Procfile`.
