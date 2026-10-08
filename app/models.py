# SQLAlchemy'dan kerakli ustun turlarini chaqiramiz
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# Database uchun asosiy Base
from .database import Base


class User(Base):
    # Foydalanuvchilar jadvali
    __tablename__ = "users"

    # Foydalanuvchi ID raqami
    id = Column(Integer, primary_key=True, index=True)

    # Foydalanuvchi nomi
    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    # Elektron pochta
    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    # Hash qilingan parol
    password = Column(
        String,
        nullable=False
    )

    # Foydalanuvchi roli
    role = Column(
        String,
        default="patient",
        nullable=False
    )


class Doctor(Base):
    # Shifokorlar jadvali
    __tablename__ = "doctors"

    # Shifokor ID raqami
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Shifokorning to'liq ismi
    full_name = Column(
        String,
        nullable=False
    )

    # Shifokorning mutaxassisligi
    specialty = Column(
        String,
        nullable=False
    )

    # Shifokorning telefon raqami
    phone = Column(
        String,
        nullable=False
    )

class Patient(Base):
    # Bemorlar jadvali
    __tablename__ = "patients"

    # Bemor ID raqami
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Bemorning to'liq ismi
    full_name = Column(
        String,
        nullable=False
    )

    # Bemorning tug'ilgan sanasi
    birth_date = Column(
        String,
        nullable=False
    )

    # Bemorning telefon raqami
    phone = Column(
        String,
        nullable=False
    )

    # Bemorning manzili
    address = Column(
        String,
        nullable=False
    )

class Appointment(Base):
    # Qabul yozuvlari jadvali
    __tablename__ = "appointments"

    # Qabul ID raqami
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Qabul qiladigan doctor ID'si
    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False
    )

    # Qabulga yozilgan patient ID'si
    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    # Qabul vaqti
    appointment_date = Column(
        DateTime,
        nullable=False
    )

    # Qabul statusi
    status = Column(
        String,
        default="pending",
        nullable=False
    )

    # Qabul sababi
    reason = Column(
        String,
        nullable=False
    )