from fastapi import FastAPI, HTTPException
from database import SessionLocal
from schemas import PatientCreate

app = FastAPI(title="Medical Management API")
@app.get("/")
def home():
    return {
        "message": " Medical Management API",
        "status": "Running Successfully"
    }


# GET ALL PATIENTS
@app.get("/patients")
def get_patients():
    conn = SessionLocal().bind.raw_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# GET PATIENT BY ID
@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    conn = SessionLocal().bind.raw_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE patient_id=%s",
        (patient_id,)
    )

    patient = cursor.fetchone()

    cursor.close()
    conn.close()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


# ADD PATIENT
@app.post("/patients")
def add_patient(patient: PatientCreate):

    conn = SessionLocal().bind.raw_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO patients
    (
        patient_name,
        age,
        gender,
        disease,
        doctor_name,
        admission_date,
        phone_number
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        patient.patient_name,
        patient.age,
        patient.gender,
        patient.disease,
        patient.doctor_name,
        patient.admission_date,
        patient.phone_number
    )

    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Patient added successfully"
    }


# UPDATE PATIENT
@app.put("/patients/{patient_id}")
def update_patient(
    patient_id: int,
    patient: PatientCreate
):

    conn = SessionLocal().bind.raw_connection()
    cursor = conn.cursor()

    query = """
    UPDATE patients
    SET
    patient_name=%s,
    age=%s,
    gender=%s,
    disease=%s,
    doctor_name=%s,
    admission_date=%s,
    phone_number=%s
    WHERE patient_id=%s
    """

    values = (
        patient.patient_name,
        patient.age,
        patient.gender,
        patient.disease,
        patient.doctor_name,
        patient.admission_date,
        patient.phone_number,
        patient_id
    )

    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Patient updated successfully"
    }


# DELETE PATIENT
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):

    conn = SessionLocal().bind.raw_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE patient_id=%s",
        (patient_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Patient deleted successfully"
    }