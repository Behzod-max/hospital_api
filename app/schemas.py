# Sana va vaqt bilan ishlash uchun
from datetime import datetime

# Appointment statuslarini cheklash uchun
from enum import Enum

# Pydantic'dan kerakli klasslarni chaqiramiz
from pydantic import BaseModel, EmailStr, ConfigDict


# =========================================================
# APPOINTMENT STATUSLARI
# =========================================================

class AppointmentStatus(str, Enum):
    # Qabul kutilmoqda
    PENDING = "pending"

    # Qabul tasdiqlangan
    CONFIRMED = "confirmed"

    # Qabul yakunlangan
    COMPLETED = "completed"

    # Qabul bekor qilingan
    CANCELLED = "cancelled"


# =========================================================
# USER SCHEMALAR
# =========================================================

class UserRoyxatdanOtish(BaseModel):
    # Foydalanuvchi nomi
    username: str

    # Elektron pochta
    email: EmailStr

    # Foydalanuvchi paroli
    password: str


class UserJavob(BaseModel):
    # Foydalanuvchi ID raqami
    id: int

    # Foydalanuvchi nomi
    username: str

    # Elektron pochta
    email: EmailStr

    # Foydalanuvchi roli
    role: str

    # SQLAlchemy obyektidan ma'lumot olishga ruxsat
    model_config = ConfigDict(from_attributes=True)


# =========================================================
# LOGIN SCHEMA
# =========================================================

class LoginSchema(BaseModel):
    # Login uchun foydalanuvchi nomi
    username: str

    # Login uchun parol
    password: str


# =========================================================
# DOCTOR SCHEMALAR
# =========================================================

class DoctorYaratish(BaseModel):
    # Doctorning to'liq ismi
    full_name: str

    # Doctorning mutaxassisligi
    specialty: str

    # Doctorning telefon raqami
    phone: str


class DoctorJavob(BaseModel):
    # Doctor ID raqami
    id: int

    # Doctorning to'liq ismi
    full_name: str

    # Doctorning mutaxassisligi
    specialty: str

    # Doctorning telefon raqami
    phone: str

    # SQLAlchemy obyektidan ma'lumot olish
    model_config = ConfigDict(from_attributes=True)


# =========================================================
# PATIENT SCHEMALAR
# =========================================================

class PatientYaratish(BaseModel):
    # Bemorning to'liq ismi
    full_name: str

    # Bemorning tug'ilgan sanasi
    birth_date: str

    # Bemorning telefon raqami
    phone: str

    # Bemorning manzili
    address: str


class PatientJavob(BaseModel):
    # Patient ID raqami
    id: int

    # Bemorning to'liq ismi
    full_name: str

    # Bemorning tug'ilgan sanasi
    birth_date: str

    # Bemorning telefon raqami
    phone: str

    # Bemorning manzili
    address: str

    # SQLAlchemy obyektidan ma'lumot olish
    model_config = ConfigDict(from_attributes=True)


# =========================================================
# APPOINTMENT SCHEMALAR
# =========================================================

class AppointmentYaratish(BaseModel):
    # Qabul qiladigan doctor ID raqami
    doctor_id: int

    # Qabulga yoziladigan patient ID raqami
    patient_id: int

    # Qabul sanasi va vaqti
    appointment_date: datetime

    # Qabulga kelish sababi
    reason: str


class AppointmentStatusOzgartrish(BaseModel):
    # Qabul statusi
    # Faqat:
    # pending
    # confirmed
    # completed
    # cancelled
    # qiymatlari qabul qilinadi
    status: AppointmentStatus


class AppointmentJavob(BaseModel):
    # Appointment ID raqami
    id: int

    # Doctor ID raqami
    doctor_id: int

    # Patient ID raqami
    patient_id: int

    # Qabul sanasi va vaqti
    appointment_date: datetime

    # Qabul statusi
    status: AppointmentStatus

    # Qabul sababi
    reason: str

    # SQLAlchemy obyektidan ma'lumot olish
    model_config = ConfigDict(from_attributes=True)