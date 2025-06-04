import sys
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime

from lib.models.medication import Category, Medication
from lib.models.dosage import Dosage
from lib.models.patient import Patient

def get_or_create_category(db: Session, name: str) -> Category:
    name = name.strip().title()
    category = db.query(Category).filter(Category.name == name).first()
    if category:
        return category
    category = Category(name=name)
    db.add(category)
    try:
        db.commit()
        db.refresh(category)
    except IntegrityError:
        db.rollback()
        category = db.query(Category).filter(Category.name == name).first()
    return category

def add_medication(db: Session, name: str, category_name: str, total_stock: int, threshold: int):
    name = name.strip().title()
    if total_stock < 0 or threshold < 0:
        raise ValueError("Stock and threshold must be non-negative integers.")
    category = get_or_create_category(db, category_name)
    new_med = Medication(
        name=name,
        category_id=category.id,
        total_stock=total_stock,
        threshold=threshold
    )
    db.add(new_med)
    try:
        db.commit()
        db.refresh(new_med)
        print(f"[+] Medication '{new_med.name}' added with ID={new_med.id}.")
    except IntegrityError:
        db.rollback()
        print(f"[!] Medication '{name}' already exists. Choose a different name.")

def list_medications(db: Session):
    meds = db.query(Medication).join(Category).all()
    if not meds:
        print("No medications found. Add one first.")
        return []
    print(f"{'ID':<4} {'NAME':<20} {'CATEGORY':<15} {'STOCK':<6} {'THRESHOLD':<9}")
    print("-" * 60)
    data = []
    for m in meds:
        data.append({
            "id": m.id,
            "name": m.name,
            "category": m.category.name,
            "stock": m.total_stock,
            "threshold": m.threshold
        })
        print(f"{m.id:<4} {m.name:<20} {m.category.name:<15} {m.total_stock:<6} {m.threshold:<9}")
    return data

def update_medication(db: Session, med_id: int, new_stock: int = None, new_threshold: int = None):
    med = db.query(Medication).filter(Medication.id == med_id).first()
    if not med:
        print(f"[!] No medication with ID={med_id}.")
        return
    if new_stock is not None:
        if new_stock < 0:
            print("[!] Stock cannot be negative.")
            return
        med.total_stock = new_stock
    if new_threshold is not None:
        if new_threshold < 0:
            print("[!] Threshold cannot be negative.")
            return
        med.threshold = new_threshold
    db.commit()
    db.refresh(med)
    print(f"[+] Medication '{med.name}' (ID={med.id}) updated. Stock={med.total_stock}, Threshold={med.threshold}.")

def delete_medication(db: Session, med_id: int):
    med = db.query(Medication).filter(Medication.id == med_id).first()
    if not med:
        print(f"[!] No medication with ID={med_id}.")
        return
    db.delete(med)
    db.commit()
    print(f"[+] Medication '{med.name}' (ID={med.id}) and its dosages have been deleted.")

def add_patient(db: Session, patient_no: str, name: str, diagnosis: str, doctor: str):
    patient_no = patient_no.strip()
    name = name.strip().title()
    diagnosis = diagnosis.strip().title()
    doctor = doctor.strip().title()
    new_patient = Patient(
        patient_no=patient_no,
        name=name,
        diagnosis=diagnosis,
        doctor=doctor
    )
    db.add(new_patient)
    try:
        db.commit()
        db.refresh(new_patient)
        print(f"[+] Patient '{new_patient.name}' created with ID={new_patient.id}.")
    except IntegrityError:
        db.rollback()
        print(f"[!] Patient No '{patient_no}' already exists. Choose a different patient number.")

def list_patients(db: Session):
    patients = db.query(Patient).all()
    if not patients:
        print("No patients found. Add one first.")
        return []
    print(f"{'ID':<4} {'PATIENT_NO':<12} {'NAME':<20} {'DIAGNOSIS':<20} {'DOCTOR':<20}")
    print("-" * 85)
    data = []
    for p in patients:
        data.append({
            "id": p.id,
            "patient_no": p.patient_no,
            "name": p.name,
            "diagnosis": p.diagnosis,
            "doctor": p.doctor
        })
        print(f"{p.id:<4} {p.patient_no:<12} {p.name:<20} {p.diagnosis:<20} {p.doctor:<20}")
    return data

def add_dosage(db: Session, med_id: int, patient_id: int, amount: int, unit: str, frequency: str):
    med = db.query(Medication).filter(Medication.id == med_id).first()
    if not med:
        print(f"[!] No medication with ID={med_id}.")
        return
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        print(f"[!] No patient with ID={patient_id}.")
        return
    if amount <= 0:
        print("[!] Dosage amount must be a positive integer.")
        return
    if med.total_stock < 1:
        print(f"[!] Not enough stock for '{med.name}'. Current stock={med.total_stock}.")
        return
    med.total_stock -= 1
    db.add(med)
    dosage = Dosage(
        medication_id=med.id,
        patient_id=patient.id,
        amount=amount,
        unit=unit.strip(),
        frequency=frequency.strip(),
        timestamp=datetime.utcnow()
    )
    db.add(dosage)
    db.commit()
    db.refresh(dosage)
    db.refresh(med)
    print(f"[+] Dosage recorded (ID={dosage.id}): {amount} {unit} of '{med.name}' for patient '{patient.name}' ({frequency}).")
    print(f"[i] New stock for '{med.name}': {med.total_stock}.")
    if med.total_stock <= med.threshold:
        print(f"[!] ALERT: '{med.name}' stock is now {med.total_stock}, which is at or below threshold ({med.threshold}).")

def list_dosages(db: Session):
    entries = (
        db.query(Dosage)
        .join(Medication)
        .join(Patient)
        .order_by(Dosage.timestamp.desc())
        .all()
    )
    if not entries:
        print("No dosages have been recorded yet.")
        return []
    print(f"{'ID':<4} {'MED_ID':<6} {'MED_NAME':<20} {'PATIENT':<20} {'AMOUNT':<8} {'UNIT':<6} {'TIME':<20} {'LOGGED_AT':<20}")
    print("-" * 117)
    data = []
    for d in entries:
        med_name = d.medication.name
        patient_name = d.patient.name
        row = {
            "id": d.id,
            "med_id": d.medication_id,
            "med_name": med_name,
            "patient_name": patient_name,
            "amount": d.amount,
            "unit": d.unit,
            "frequency": d.frequency,
            "timestamp": d.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(row)
        print(f"{d.id:<4} {d.medication_id:<6} {med_name:<20} {patient_name:<20} {d.amount:<8} {d.unit:<6} {d.frequency:<20} {row['timestamp']:<20}")
    return data

def check_refills(db: Session):
    meds = db.query(Medication).all()
    low_stock = []
    for m in meds:
        if m.total_stock <= m.threshold:
            low_stock.append({
                "id": m.id,
                "name": m.name,
                "stock": m.total_stock,
                "threshold": m.threshold
            })
    if not low_stock:
        print("All medications are above their threshold. No low-stock alerts.")
        return low_stock
    print(f"{'ID':<4} {'NAME':<20} {'STOCK':<6} {'THRESHOLD':<9}")
    print("-" * 45)
    for item in low_stock:
        print(f"{item['id']:<4} {item['name']:<20} {item['stock']:<6} {item['threshold']:<9}")
    return low_stock

def get_medication_by_id(db: Session, med_id: int) -> Medication:
    return db.query(Medication).filter(Medication.id == med_id).first()

def safe_int_input(prompt: str) -> int:
    while True:
        val = input(prompt).strip()
        if not val.isdigit():
            print("[!] Please enter a valid integer.")
            continue
        return int(val)
