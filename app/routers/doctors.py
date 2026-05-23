from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.DoctorOut])
def get_all_doctors(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()


@router.get("/{doctor_id}", response_model=schemas.DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.post("/", response_model=schemas.DoctorOut, status_code=201)
def create_doctor(payload: schemas.DoctorCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Doctor).filter(models.Doctor.prc_license_no == payload.prc_license_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="PRC license number already registered")
    doctor = models.Doctor(**payload.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.put("/{doctor_id}", response_model=schemas.DoctorOut)
def update_doctor(doctor_id: int, payload: schemas.DoctorUpdate, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    data = payload.model_dump(exclude_none=True)
    if data.get("prc_license_no") is not None:
        existing = db.query(models.Doctor).filter(
            models.Doctor.prc_license_no == data["prc_license_no"],
            models.Doctor.doctor_id != doctor_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="PRC license number already registered")
    for key, value in data.items():
        setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.delete("/{doctor_id}", status_code=204)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
