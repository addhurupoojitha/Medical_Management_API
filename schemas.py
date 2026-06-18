from pydantic import BaseModel
from datetime import date

class PatientCreate(BaseModel):
    patient_name: str
    age: int
    gender: str
    disease: str
    doctor_name: str
    admission_date: date
    phone_number: str