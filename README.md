# Bookit

Lightweight Django + DRF project for managing occasions and reservations.

This repository includes DRF endpoints and Swagger/OpenAPI documentation powered by `drf_yasg`.

## Prerequisites

- Python 3.11+ (project was tested with Python 3.11/3.12/3.13)
- PostgreSQL (or adjust `DATABASES` in `bookit/settings.py` to use sqlite for local dev)
- A virtual environment (recommended)

## Quick setup (development)

All commands assume you're at the project root (`/home/brandon/Papyrus/bookit`) and you have an activated venv. If you don't have a venv yet:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root or set environment variables. The project uses `python-decouple` so environment variables referenced in `bookit/settings.py` are:

- DB_NAME (default: `bookit_db`)
- DB_USER (default: `postgres`)
- DB_PASSWORD
- DB_HOST (default: `localhost`)
- DB_PORT (default: `5432`)
- SECRET_KEY (optional; a default is present in settings for development)
- DEBUG (set to `True` for local development)

Example `.env` contents:

```env
DB_NAME=bookit_db
DB_USER=postgres
DB_PASSWORD=postgres_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key
DEBUG=True
```

Run database migrations:

```bash
python manage.py migrate
```

Create a superuser (optional):

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

## API documentation (Swagger / Redoc)

While `DEBUG=True`, interactive documentation is available at:

- Swagger UI: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/
- Raw OpenAPI JSON: http://127.0.0.1:8000/swagger.json

The Swagger UI includes an "Authorize" button. This project uses JWT tokens (Simple JWT). After logging in (see below) copy the `access` token and open Authorize, then paste the token prefixed with `Bearer ` (including the space). Example:

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...rest_of_token
```

If you paste only the raw token the server will reject it with "Authentication credentials were not provided." — the `Bearer ` prefix is required.

## Authentication endpoints

- Register: POST `/auth/register` (see `authentication.serializers.UserRegistrationSerializer` for fields)
- Login: POST `/auth/login` (returns `access` and `refresh` tokens)
- Profile: GET `/auth/profile` (requires Authorization header)

Example curl for login (returns tokens):

```bash
curl -X POST -H "Content-Type: application/json" -d '{"email":"you@example.com","password":"yourpassword"}' http://127.0.0.1:8000/auth/login
```

Use the returned `access` token in the Swagger UI or include it in requests:

```bash
curl -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/occasions/
```

## Important notes & troubleshooting

- Make sure to use the `access` token (not the refresh token) when calling protected endpoints.
- Ensure there are no stray quotes or whitespace when pasting the token into the Authorize dialog.
- If an endpoint shows no parameters in the Swagger UI, ensure the view has been annotated with `swagger_auto_schema` or the serializer is present for request/response bodies. The project includes basic annotations to expose path/query/request bodies.
- To restrict documentation in production, remove or protect the swagger routes in `bookit/urls.py` (currently they are only added when `DEBUG` is True).

