from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.BillingOut])
def get_all_billings(db: Session = Depends(get_db)):
    return db.query(models.Billing).all()


@router.get("/{billing_id}", response_model=schemas.BillingOut)
def get_billing(billing_id: int, db: Session = Depends(get_db)):
    billing = db.query(models.Billing).filter(models.Billing.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing record not found")
    return billing


@router.post("/", response_model=schemas.BillingOut, status_code=201)
def create_billing(payload: schemas.BillingCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    visit = db.query(models.Visit).filter(models.Visit.visit_id == data["visit_id"]).first()
    if not visit:
        raise HTTPException(status_code=400, detail="Visit not found for this billing")
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == data["doctor_id"]).first()
    if not doctor:
        raise HTTPException(status_code=400, detail="Doctor not found for this billing")
    billing = models.Billing(**data)
    db.add(billing)
    db.commit()
    db.refresh(billing)
    return billing


@router.put("/{billing_id}", response_model=schemas.BillingOut)
def update_billing(billing_id: int, payload: schemas.BillingUpdate, db: Session = Depends(get_db)):
    billing = db.query(models.Billing).filter(models.Billing.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing record not found")
    data = payload.model_dump(exclude_none=True)
    if data.get("visit_id") is not None:
        visit = db.query(models.Visit).filter(models.Visit.visit_id == data["visit_id"]).first()
        if not visit:
            raise HTTPException(status_code=400, detail="Visit not found for this billing")
    if data.get("doctor_id") is not None:
        doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == data["doctor_id"]).first()
        if not doctor:
            raise HTTPException(status_code=400, detail="Doctor not found for this billing")
    for key, value in data.items():
        setattr(billing, key, value)
    db.commit()
    db.refresh(billing)
    return billing


@router.delete("/{billing_id}", status_code=204)
def delete_billing(billing_id: int, db: Session = Depends(get_db)):
    billing = db.query(models.Billing).filter(models.Billing.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing record not found")
    db.delete(billing)
    db.commit()
