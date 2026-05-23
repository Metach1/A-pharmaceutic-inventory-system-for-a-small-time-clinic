from sqlalchemy import (
    Column, Integer, String, Numeric, Date, Text,
    TIMESTAMP, CHAR, Enum, ForeignKey
)
from app.database import Base
import enum


# ── Enums ──────────────────────────────────────────────────────────────────────

class DosageForm(str, enum.Enum):
    tablet    = "tablet"
    capsule   = "capsule"
    syrup     = "syrup"
    injection = "injection"
    ointment  = "ointment"


class RegClass(str, enum.Enum):
    prescription = "prescription"
    otc          = "otc"
    controlled   = "controlled"


class PaymentMethod(str, enum.Enum):
    cash       = "cash"
    philhealth = "philhealth"
    card       = "card"
    hmo        = "hmo"


# ── Models ─────────────────────────────────────────────────────────────────────

class Drug(Base):
    __tablename__ = "drug"

    drug_id       = Column(Integer, primary_key=True, index=True, autoincrement=True)
    generic_name  = Column(String(100), nullable=False)
    brand_name    = Column(String(100))
    dosage_form   = Column(Enum(DosageForm))
    reg_class     = Column(Enum(RegClass))
    supplier_id   = Column(Integer)
    reorder_level = Column(Integer)


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id   = Column(Integer, primary_key=True, index=True, autoincrement=True)
    drug_id        = Column(Integer, ForeignKey("drug.drug_id"), nullable=False)
    quantity       = Column(Integer)
    unit_cost      = Column(Numeric(10, 2))
    unit_price     = Column(Numeric(10, 2))
    buy_date       = Column(Date)
    expiry_date    = Column(Date)
    last_restocked = Column(Date)


class Patient(Base):
    __tablename__ = "patient"

    patient_id    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name     = Column(String(150), nullable=False)
    date_of_birth = Column(Date)
    sex           = Column(CHAR(1))
    address       = Column(String(255))
    phone         = Column(String(20))
    philhealth_no = Column(String(50))
    created_at    = Column(TIMESTAMP)


class Doctor(Base):
    __tablename__ = "doctor"

    doctor_id      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name      = Column(String(150), nullable=False)
    prc_license_no = Column(String(50), unique=True, nullable=False)
    specialization = Column(String(100))
    phone          = Column(String(20))


class Visit(Base):
    __tablename__ = "visit"

    visit_id   = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_id  = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    visit_date = Column(TIMESTAMP)
    notes      = Column(Text)


class Prescription(Base):
    __tablename__ = "prescription"

    prescription_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    visit_id        = Column(Integer, ForeignKey("visit.visit_id"), nullable=False)
    drug_id         = Column(Integer, ForeignKey("drug.drug_id"), nullable=False)
    instruction     = Column(Text)
    qty_prescribed  = Column(Integer, nullable=False)


class Billing(Base):
    __tablename__ = "billing"

    billing_id     = Column(Integer, primary_key=True, index=True, autoincrement=True)
    visit_id       = Column(Integer, ForeignKey("visit.visit_id"), nullable=False)
    doctor_id      = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=False)
    total_fee      = Column(Numeric(10, 2))
    payment_method = Column(Enum(PaymentMethod))
    paid_on        = Column(Date)
