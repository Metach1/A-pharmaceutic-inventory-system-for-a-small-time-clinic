from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import drugs, inventory, patients, doctors, visits, prescriptions, billings

# Auto-creates all tables in the database on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clinic Management API",
    description="REST API for managing drugs, patients, doctors, visits, prescriptions, and billing.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drugs.router,         prefix="/drugs",         tags=["Drugs"])
app.include_router(inventory.router,     prefix="/inventory",     tags=["Inventory"])
app.include_router(patients.router,      prefix="/patients",      tags=["Patients"])
app.include_router(doctors.router,       prefix="/doctors",       tags=["Doctors"])
app.include_router(visits.router,        prefix="/visits",        tags=["Visits"])
app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(billings.router,      prefix="/billings",      tags=["Billings"])


@app.get("/", tags=["Root"])
def root():
    return {"message": "Clinic Management API is running ✅"}
