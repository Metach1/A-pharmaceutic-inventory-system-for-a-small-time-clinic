# Clinic Management System

A student-friendly FastAPI + MySQL CRUD application with a simple JavaScript frontend.

## What this app does

This project supports CRUD operations for the following entities:

- **Drug** — medicine master data
- **Inventory** — drug stock records
- **Patient** — patient personal data
- **Doctor** — doctor personal data
- **Visit** — patient visit records
- **Prescription** — medicines prescribed for a visit
- **Billing** — payment records for a visit

## Entity relationships

- A **Patient** can have many **Visits**.
- A **Doctor** can have many **Visits**.
- A **Visit** can have multiple **Prescriptions**.
- A **Drug** can appear in many **Prescriptions**.
- A **Drug** can have multiple **Inventory** records.
- A **Visit** can have one **Billing** record.
- A **Doctor** can appear in many **Billings**.

## Project structure

- `app/` - backend Python package
- `app/main.py` - FastAPI app and router registration
- `app/database.py` - SQLAlchemy connection and session helper
- `app/models.py` - database models for all entities
- `app/schemas.py` - Pydantic models for API requests and responses
- `app/routers/` - one router per entity with CRUD endpoints
- `frontend/index.html` - student-friendly UI for CRUD operations
- `.env` - database configuration
- `requirements.txt` - Python package list
- `.env.example` - example database config

## How to run it

### 1. Activate the virtual environment

From the project root folder:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create the MySQL database

Use MySQL Workbench or the MySQL command line to create `clinic_db`:

```sql
CREATE DATABASE clinic_db;
```

### 4. Configure `.env`

Open `.env` and set your MySQL username, password, host, port, and database name:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/clinic_db
DEBUG=1
```

- `DEBUG=1` turns on SQL logging in the backend.
- If `.env` is missing or invalid, the app will show a clear error.

### 5. Run the backend

```bash
uvicorn app.main:app --reload
```

Open these pages in your browser:

- `http://localhost:8000` — API root
- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/redoc` — ReDoc docs

### 6. Open the frontend

Open `frontend/index.html` in your browser.

In the page, set the API Base URL to:

```text
http://localhost:8000
```

Then use the menu to browse and manage records.

## CRUD usage flow

Because of foreign keys, create records in this order first:

1. **Drug**
2. **Patient**
3. **Doctor**
4. **Visit** (needs doctor_id and patient_id)
5. **Prescription** (needs visit_id and drug_id)
6. **Billing** (needs visit_id and doctor_id)

The frontend lets you add, edit, and delete records for all entities.

## Example endpoints

- `GET /drugs/`
- `POST /drugs/`
- `PUT /drugs/{drug_id}`
- `DELETE /drugs/{drug_id}`

- `GET /patients/`
- `POST /patients/`
- `PUT /patients/{patient_id}`
- `DELETE /patients/{patient_id}`

- `GET /visits/`
- `POST /visits/`
- `PUT /visits/{visit_id}`
- `DELETE /visits/{visit_id}`

- `GET /billings/`
- `POST /billings/`
- `PUT /billings/{billing_id}`
- `DELETE /billings/{billing_id}`

## Debugging tips

- If the backend fails to start, check `.env` and `DATABASE_URL`.
- If the browser frontend fails, make sure the backend is running at `http://localhost:8000`.
- Use `http://localhost:8000/docs` to test APIs and inspect required fields.
- Run the app in the same terminal where `uvicorn` is started so you can see error messages immediately.

## Manual IDs (optional)

- The database tables use auto-increment primary keys (e.g. `drug_id`, `inventory_id`).
- The frontend now allows you to optionally type an ID when creating `drug` or `inventory` records. If you leave the ID field blank, the database will auto-assign the next value.
- If you provide an explicit ID, make sure it does not already exist in the table (the API will return an error for duplicates).


## Student-friendly notes

- The backend is already split into small routers, one per entity.
- The frontend loads data from the API and sends JSON requests for add/edit/delete.
- If you want, we can add validation in the frontend so you cannot submit wrong IDs or empty required fields.
