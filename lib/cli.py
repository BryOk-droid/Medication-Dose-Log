import sys
from sqlalchemy.orm import Session

from lib.models import init_db, SessionLocal
from lib.models.medication import Medication
from lib.models.dosage import Dosage
from lib.models.patient import Patient

from lib.helpers import (
    add_medication,
    list_medications,
    update_medication,
    delete_medication,
    add_patient,
    list_patients,
    add_dosage,
    list_dosages,
    check_refills,
    safe_int_input
)

def print_menu():
    menu_options = (
        ("1", "List Medications"),
        ("2", "List All Dosages"),
        ("3", "Add Medication"),
        ("4", "Update Medication Stock/Threshold"),
        ("5", "Add Dosage"),
        ("6", "Check Low-Stock Alerts"),
        ("7", "Add Patient"),
        ("8", "List Patients"),
        ("9", "Delete Medication"),
        ("10","Exit"),
    )
    print("\n=== Medication Dosage Log CLI ===")
    for key, desc in menu_options:
        print(f"{key}. {desc}")
    print("----------------------------------")

def main():
    init_db()
    db: Session = SessionLocal()

    while True:
        print_menu()
        choice = input("Select an option [1-10]: ").strip()

        if choice == "1":
            list_medications(db)

        elif choice == "2":
            list_dosages(db)

        elif choice == "3":
            print("\n--- Add Medication ---")
            name = input("Medication name: ").strip()
            category = input("Category: ").strip()
            total_stock = safe_int_input("Total stock (integer): ")
            threshold = safe_int_input("Low‐stock threshold (integer): ")
            try:
                add_medication(db, name, category, total_stock, threshold)
            except ValueError as ve:
                print(f"[!] {ve}")

        elif choice == "4":
            print("\n--- Update Medication ---")
            meds = list_medications(db)
            if not meds:
                continue
            med_id = safe_int_input("Enter the ID of the medication to update: ")
            new_stock = safe_int_input("New stock (leave blank to skip)? ")
            new_threshold = safe_int_input("New threshold (leave blank to skip)? ")
            update_medication(db, med_id, new_stock, new_threshold)

        elif choice == "5":
            print("\n--- Add Dosage ---")
            meds = list_medications(db)
            if not meds:
                continue
            patients = list_patients(db)
            if not patients:
                print("[!] No patients exist. Please add one first.")
                continue
            med_id = safe_int_input("Medication ID: ")
            patient_id = safe_int_input("Patient ID: ")
            amount = safe_int_input("Dosage amount (integer): ")
            unit = input("Dosage unit (e.g. mg, pill): ").strip()
            frequency = input("Time of day (e.g. morning, evening, after meals): ").strip()
            add_dosage(db, med_id, patient_id, amount, unit, frequency)

        elif choice == "6":
            print("\n--- Low-Stock Alerts ---")
            check_refills(db)

        elif choice == "7":
            print("\n--- Add Patient ---")
            patient_no = input("Patient No (unique): ").strip()
            name = input("Patient name: ").strip()
            diagnosis = input("Diagnosis: ").strip()
            doctor = input("Prescribing doctor: ").strip()
            add_patient(db, patient_no, name, diagnosis, doctor)

        elif choice == "8":
            print("\n--- List Patients ---")
            list_patients(db)

        elif choice == "9":
            print("\n--- Delete Medication ---")
            meds = list_medications(db)
            if not meds:
                continue
            med_id = safe_int_input("ID of medication to delete: ")
            delete_medication(db, med_id)

        elif choice == "10":
            print("Exiting. Goodbye!")
            db.close()
            sys.exit(0)

        else:
            print("[!] Invalid option. Please choose a number between 1 and 10.")

if __name__ == "__main__":
    main()
