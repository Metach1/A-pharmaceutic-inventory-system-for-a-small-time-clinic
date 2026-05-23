from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.VisitOut])
def get_all_visits(db: Session = Depends(get_db)):
    return db.query(models.Visit).all()


@router.get("/{visit_id}", response_model=schemas.VisitOut)
def get_visit(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(models.Visit).filter(models.Visit.visit_id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@router.post("/", response_model=schemas.VisitOut, status_code=201)
def create_visit(payload: schemas.VisitCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == data["doctor_id"]).first()
    if not doctor:
        raise HTTPException(status_code=400, detail="Doctor not found for this visit")
    patient = db.query(models.Patient).filter(models.Patient.patient_id == data["patient_id"]).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient not found for this visit")
    visit = models.Visit(**data)
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


@router.put("/{visit_id}", response_model=schemas.VisitOut)
def update_visit(visit_id: int, payload: schemas.VisitUpdate, db: Session = Depends(get_db)):
    visit = db.query(models.Visit).filter(models.Visit.visit_id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    data = payload.model_dump(exclude_none=True)
    if data.get("doctor_id") is not None:
        doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == data["doctor_id"]).first()
        if not doctor:
            raise HTTPException(status_code=400, detail="Doctor not found for this visit")
    if data.get("patient_id") is not None:
        patient = db.query(models.Patient).filter(models.Patient.patient_id == data["patient_id"]).first()
        if not patient:
            raise HTTPException(status_code=400, detail="Patient not found for this visit")
    for key, value in data.items():
        setattr(visit, key, value)
    db.commit()
    db.refresh(visit)
    return visit


@router.delete("/{visit_id}", status_code=204)
def delete_visit(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(models.Visit).filter(models.Visit.visit_id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    db.delete(visit)
    db.commit()
