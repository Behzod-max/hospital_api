from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Appointment, Doctor, Patient
from ..schemas import (
    AppointmentYaratish,
    AppointmentJavob,
    AppointmentStatusOzgartrish
)
from ..auth import get_current_user


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# =========================================================
# APPOINTMENT YARATISH
# =========================================================

@router.post(
    "/",
    response_model=AppointmentJavob,
    status_code=status.HTTP_201_CREATED
)
def appointment_yaratish(
    appointment: AppointmentYaratish,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Doctor mavjudligini tekshirish
    doctor = db.query(Doctor).filter(
        Doctor.id == appointment.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor topilmadi"
        )

    # Patient mavjudligini tekshirish
    patient = db.query(Patient).filter(
        Patient.id == appointment.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient topilmadi"
        )

    # Doctor shu vaqtda bandligini tekshirish
    mavjud_appointment = db.query(Appointment).filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.appointment_date == appointment.appointment_date,
        Appointment.status != "cancelled"
    ).first()

    if mavjud_appointment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor bu vaqtda band"
        )

    # Yangi appointment
    yangi_appointment = Appointment(
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        appointment_date=appointment.appointment_date,
        status="pending",
        reason=appointment.reason
    )

    db.add(yangi_appointment)
    db.commit()
    db.refresh(yangi_appointment)

    return yangi_appointment


# =========================================================
# BARCHA APPOINTMENTLAR
# =========================================================

@router.get(
    "/",
    response_model=list[AppointmentJavob]
)
def appointmentlar_royxati(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Appointment).order_by(
        Appointment.appointment_date
    ).all()


# =========================================================
# DOCTOR BO'YICHA FILTER
# =========================================================

@router.get(
    "/doctor/{doctor_id}",
    response_model=list[AppointmentJavob]
)
def doctor_appointmentlari(
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

    return db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id
    ).order_by(
        Appointment.appointment_date
    ).all()


# =========================================================
# APPOINTMENT HISTORY
# =========================================================

@router.get(
    "/history",
    response_model=list[AppointmentJavob]
)
def appointment_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Appointment).filter(
        Appointment.status.in_([
            "completed",
            "cancelled"
        ])
    ).order_by(
        Appointment.appointment_date.desc()
    ).all()


# =========================================================
# STATUSNI O'ZGARTIRISH
# =========================================================

@router.patch(
    "/{appointment_id}/status",
    response_model=AppointmentJavob
)
def appointment_statusini_ozgartirish(
    appointment_id: int,
    status_data: AppointmentStatusOzgartrish,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment topilmadi"
        )

    appointment.status = status_data.status.value

    db.commit()
    db.refresh(appointment)

    return appointment


# =========================================================
# BITTA APPOINTMENT
# =========================================================

@router.get(
    "/{appointment_id}",
    response_model=AppointmentJavob
)
def appointment_detail(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment topilmadi"
        )

    return appointment