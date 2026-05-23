from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.PrescriptionOut])
def get_all_prescriptions(db: Session = Depends(get_db)):
    return db.query(models.Prescription).all()


@router.get("/{prescription_id}", response_model=schemas.PrescriptionOut)
def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    rx = db.query(models.Prescription).filter(models.Prescription.prescription_id == prescription_id).first()
    if not rx:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return rx


@router.post("/", response_model=schemas.PrescriptionOut, status_code=201)
def create_prescription(payload: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    visit = db.query(models.Visit).filter(models.Visit.visit_id == data["visit_id"]).first()
    if not visit:
        raise HTTPException(status_code=400, detail="Visit not found for this prescription")
    drug = db.query(models.Drug).filter(models.Drug.drug_id == data["drug_id"]).first()
    if not drug:
        raise HTTPException(status_code=400, detail="Drug not found for this prescription")
    rx = models.Prescription(**data)
    db.add(rx)
    db.commit()
    db.refresh(rx)
    return rx


@router.put("/{prescription_id}", response_model=schemas.PrescriptionOut)
def update_prescription(prescription_id: int, payload: schemas.PrescriptionUpdate, db: Session = Depends(get_db)):
    rx = db.query(models.Prescription).filter(models.Prescription.prescription_id == prescription_id).first()
    if not rx:
        raise HTTPException(status_code=404, detail="Prescription not found")
    data = payload.model_dump(exclude_none=True)
    if data.get("visit_id") is not None:
        visit = db.query(models.Visit).filter(models.Visit.visit_id == data["visit_id"]).first()
        if not visit:
            raise HTTPException(status_code=400, detail="Visit not found for this prescription")
    if data.get("drug_id") is not None:
        drug = db.query(models.Drug).filter(models.Drug.drug_id == data["drug_id"]).first()
        if not drug:
            raise HTTPException(status_code=400, detail="Drug not found for this prescription")
    for key, value in data.items():
        setattr(rx, key, value)
    db.commit()
    db.refresh(rx)
    return rx


@router.delete("/{prescription_id}", status_code=204)
def delete_prescription(prescription_id: int, db: Session = Depends(get_db)):
    rx = db.query(models.Prescription).filter(models.Prescription.prescription_id == prescription_id).first()
    if not rx:
        raise HTTPException(status_code=404, detail="Prescription not found")
    db.delete(rx)
    db.commit()
