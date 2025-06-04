# Medication Dosage Log CLI

A terminal-based Python application to manage patient medication schedules, stock levels, and dosage logs. Data is stored in a local SQLite database (`medication_log.db`) via SQLAlchemy ORM.

## Features

- **Patients**:  
  - Register by **Patient No.**, **Name**, **Diagnosis**, **Prescribing Doctor**  
  - List all patients  

- **Medications**:  
  - Add by **Name**, **Category**, **Total Stock**, **Low-Stock Threshold**  
  - Update stock/threshold  
  - List all medications  
  - Delete a medication (cascading its dosage records)  

- **Dosage Logging**:  
  - Log a dose for a given patient & medication: enter **Amount**, **Unit**, **Time of Day**  
  - Automatically deduct one pill from stock per log  
  - List all dosage records (shows medication, patient, dose, time, timestamp)  
  - Alert when stock ≤ threshold  

## Prerequisites

- Python 3.8+  
- Pipenv (for virtual environment)  
- Git

## Installation

```bash
git clone https://github.com/BryOk-droid/medication-dose-log.git
cd medication-dose-log
pipenv install
pipenv shell
python - <<EOF
from lib.models import init_db
init_db()
EOF
```
## Database Schema & Relationships

### patients
- `id` (PK)  
- `patient_no` (unique)  
- `name`  
- `diagnosis`  
- `doctor`  

† 1 patient → *many* dosages

### categories
- `id` (PK)  
- `name` (unique)  

† 1 category → *many* medications

### medications
- `id` (PK)  
- `name` (unique)  
- `category_id` (FK)  
- `total_stock`  
- `threshold`  

† 1 medication → *many* dosages

### dosages
- `id` (PK)  
- `medication_id` (FK)  
- `patient_id` (FK)  
- `amount`  
- `unit`  
- `frequency`  
- `timestamp`  

Links each dosage to one medication and one patient

---

## Usage

### Launch the CLI
```bash
pipenv run python -m lib.cli
```
## Menu Options

- List Medications  
- List All Dosages  
- Add Medication  
- Update Medication Stock/Threshold  
- Add Dosage  
- Check Low-Stock Alerts  
- Add Patient  
- List Patients  
- Delete Medication  
- Exit  

---

## Troubleshooting

| Issue                   | Solution                                    |
|-------------------------|---------------------------------------------|
| Database not updating   | Run `rm medication_log.db` and restart      |
| Invalid input errors    | Follow prompts for correct formats          |
| SQLite inspection       | Use `sqlite3 medication_log.db`             |

## Author

👤 **Brian Omuga**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/BryOk-droid)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/brianokoth/)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://bryok-droid.github.io/Personal-Portfolio/)

- **Email**: brianomugah@gmail.com  
- **Project Link**: [https://github.com/BryOk-droid/Medication-dose-log](https://github.com/BryOk-droid/Medication-dose-log)

## License

MIT License

Copyright (c) 2023 BryOk-droid

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

