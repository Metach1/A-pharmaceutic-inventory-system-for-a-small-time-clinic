from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.DrugOut])
def get_all_drugs(db: Session = Depends(get_db)):
    return db.query(models.Drug).all()


@router.get("/{drug_id}", response_model=schemas.DrugOut)
def get_drug(drug_id: int, db: Session = Depends(get_db)):
    drug = db.query(models.Drug).filter(models.Drug.drug_id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return drug


@router.post("/", response_model=schemas.DrugOut, status_code=201)
def create_drug(payload: schemas.DrugCreate, db: Session = Depends(get_db)):
    drug = models.Drug(**payload.model_dump())
    db.add(drug)
    db.commit()
    db.refresh(drug)
    return drug


@router.put("/{drug_id}", response_model=schemas.DrugOut)
def update_drug(drug_id: int, payload: schemas.DrugUpdate, db: Session = Depends(get_db)):
    drug = db.query(models.Drug).filter(models.Drug.drug_id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(drug, key, value)
    db.commit()
    db.refresh(drug)
    return drug


@router.delete("/{drug_id}", status_code=204)
def delete_drug(drug_id: int, db: Session = Depends(get_db)):
    drug = db.query(models.Drug).filter(models.Drug.drug_id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    db.delete(drug)
    db.commit()
