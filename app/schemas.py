from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models import DosageForm, RegClass, PaymentMethod


# ── Drug ───────────────────────────────────────────────────────────────────────

class DrugBase(BaseModel):
    generic_name:  str
    brand_name:    Optional[str] = None
    dosage_form:   Optional[DosageForm] = None
    reg_class:     Optional[RegClass] = None
    supplier_id:   Optional[int] = None
    reorder_level: Optional[int] = None

class DrugCreate(DrugBase):
    drug_id: Optional[int] = None

class DrugUpdate(BaseModel):
    generic_name: Optional[str] = None
    brand_name: Optional[str] = None
    dosage_form: Optional[DosageForm] = None
    reg_class: Optional[RegClass] = None
    supplier_id: Optional[int] = None
    reorder_level: Optional[int] = None

class DrugOut(DrugBase):
    drug_id: int
    class Config:
        from_attributes = True


# ── Inventory ──────────────────────────────────────────────────────────────────

class InventoryBase(BaseModel):
    drug_id:        int
    quantity:       Optional[int] = None
    unit_cost:      Optional[float] = None
    unit_price:     Optional[float] = None
    buy_date:       Optional[date] = None
    expiry_date:    Optional[date] = None
    last_restocked: Optional[date] = None

class InventoryCreate(InventoryBase):
    inventory_id: Optional[int] = None

class InventoryUpdate(BaseModel):
    drug_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_cost: Optional[float] = None
    unit_price: Optional[float] = None
    buy_date: Optional[date] = None
    expiry_date: Optional[date] = None
    last_restocked: Optional[date] = None

class InventoryOut(InventoryBase):
    inventory_id: int
    class Config:
        from_attributes = True


# ── Patient ────────────────────────────────────────────────────────────────────

class PatientBase(BaseModel):
    full_name:     str
    date_of_birth: Optional[date] = None
    sex:           Optional[str] = None
    address:       Optional[str] = None
    phone:         Optional[str] = None
    philhealth_no: Optional[str] = None
    created_at:    Optional[datetime] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    sex: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    philhealth_no: Optional[str] = None
    created_at: Optional[datetime] = None

class PatientOut(PatientBase):
    patient_id: int
    class Config:
        from_attributes = True


# ── Doctor ─────────────────────────────────────────────────────────────────────

class DoctorBase(BaseModel):
    full_name:      str
    prc_license_no: str
    specialization: Optional[str] = None
    phone:          Optional[str] = None

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    prc_license_no: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None

class DoctorOut(DoctorBase):
    doctor_id: int
    class Config:
        from_attributes = True


# ── Visit ──────────────────────────────────────────────────────────────────────

class VisitBase(BaseModel):
    doctor_id:  int
    patient_id: int
    visit_date: Optional[datetime] = None
    notes:      Optional[str] = None

class VisitCreate(VisitBase):
    pass

class VisitUpdate(BaseModel):
    doctor_id: Optional[int] = None
    patient_id: Optional[int] = None
    visit_date: Optional[datetime] = None
    notes: Optional[str] = None

class VisitOut(VisitBase):
    visit_id: int
    class Config:
        from_attributes = True


# ── Prescription ───────────────────────────────────────────────────────────────

class PrescriptionBase(BaseModel):
    visit_id:       int
    drug_id:        int
    instruction:    Optional[str] = None
    qty_prescribed: int

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(BaseModel):
    visit_id: Optional[int] = None
    drug_id: Optional[int] = None
    instruction: Optional[str] = None
    qty_prescribed: Optional[int] = None

class PrescriptionOut(PrescriptionBase):
    prescription_id: int
    class Config:
        from_attributes = True


# ── Billing ────────────────────────────────────────────────────────────────────

class BillingBase(BaseModel):
    visit_id:       int
    doctor_id:      int
    total_fee:      Optional[float] = None
    payment_method: Optional[PaymentMethod] = None
    paid_on:        Optional[date] = None

class BillingCreate(BillingBase):
    pass

class BillingUpdate(BaseModel):
    visit_id: Optional[int] = None
    doctor_id: Optional[int] = None
    total_fee: Optional[float] = None
    payment_method: Optional[PaymentMethod] = None
    paid_on: Optional[date] = None

class BillingOut(BillingBase):
    billing_id: int
    class Config:
        from_attributes = True
