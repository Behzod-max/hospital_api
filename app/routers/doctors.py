from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Doctor
from ..schemas import DoctorYaratish, DoctorJavob
from ..auth import get_current_user
from ..auth import role_required

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


# Doctor yaratish
@router.post(
    "/",
    response_model=DoctorJavob,
    status_code=status.HTTP_201_CREATED
)
def doctor_yaratish(
    doctor: DoctorYaratish,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    yangi_doctor = Doctor(
        full_name=doctor.full_name,
        specialty=doctor.specialty,
        phone=doctor.phone
    )

    db.add(yangi_doctor)
    db.commit()
    db.refresh(yangi_doctor)

    return yangi_doctor


# Doctorlar ro'yxati
@router.get(
    "/",
    response_model=list[DoctorJavob]
)
def doctorlar_royxati(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Doctor).all()


# Bitta doctor
@router.get(
    "/{doctor_id}",
    response_model=DoctorJavob
)
def doctor_detail(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor topilmadi"
        )

    return doctor