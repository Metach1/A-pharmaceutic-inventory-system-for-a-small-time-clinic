from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.InventoryOut])
def get_all_inventory(db: Session = Depends(get_db)):
    return db.query(models.Inventory).all()


@router.get("/{inventory_id}", response_model=schemas.InventoryOut)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Inventory).filter(models.Inventory.inventory_id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return item


@router.post("/", response_model=schemas.InventoryOut, status_code=201)
def create_inventory(payload: schemas.InventoryCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    drug = db.query(models.Drug).filter(models.Drug.drug_id == data["drug_id"]).first()
    if not drug:
        raise HTTPException(status_code=400, detail="Drug not found for this inventory record")
    item = models.Inventory(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{inventory_id}", response_model=schemas.InventoryOut)
def update_inventory(inventory_id: int, payload: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    item = db.query(models.Inventory).filter(models.Inventory.inventory_id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    data = payload.model_dump(exclude_none=True)
    if data.get("drug_id") is not None:
        drug = db.query(models.Drug).filter(models.Drug.drug_id == data["drug_id"]).first()
        if not drug:
            raise HTTPException(status_code=400, detail="Drug not found for this inventory record")
    for key, value in data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{inventory_id}", status_code=204)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Inventory).filter(models.Inventory.inventory_id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    db.delete(item)
    db.commit()
