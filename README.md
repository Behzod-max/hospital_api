# 🏥 Hospital Patient API

FastAPI va PostgreSQL asosida yaratilgan kasalxona boshqaruv API.

## 🚀 Texnologiyalar

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT Authentication
- Passlib
- Pydantic
- Swagger UI

## 📌 Imkoniyatlar

### Authentication
- User registration
- User login
- JWT authentication
- Role-based access

### Doctors
- Doctor yaratish
- Doctorlar ro'yxati
- Doctor detail

### Patients
- Patient yaratish
- Patientlar ro'yxati
- Patient detail

### Appointments
- Appointment yaratish
- Appointmentlar ro'yxati
- Appointment detail
- Doctor bo'yicha filter
- Appointment history
- Statusni o'zgartirish
- Bir doctorni bir xil vaqtda ikki patient band qilishini bloklash

## 📁 Loyiha strukturasi

```text
hospital_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── doctors.py
│       ├── patients.py
│       └── appointments.py
│
├── alembic/
├── .env
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md