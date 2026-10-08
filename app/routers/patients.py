from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Patient
from ..schemas import PatientYaratish, PatientJavob
from ..auth import get_current_user


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# Patient yaratish
@router.post(
    "/",
    response_model=PatientJavob,
    status_code=status.HTTP_201_CREATED
)
def patient_yaratish(
    patient: PatientYaratish,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    yangi_patient = Patient(
        full_name=patient.full_name,
        birth_date=patient.birth_date,
        phone=patient.phone,
        address=patient.address
    )

    db.add(yangi_patient)
    db.commit()
    db.refresh(yangi_patient)

    return yangi_patient


# Patientlar ro'yxati
@router.get(
    "/",
    response_model=list[PatientJavob]
)
def patientlar_royxati(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Patient).all()


# Bitta patient
@router.get(
    "/{patient_id}",
    response_model=PatientJavob
)
def patient_detail(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient topilmadi"
        )

    return patient