from fastapi import FastAPI, Depends

from .routers import (
    auth,
    doctors,
    patients,
    appointments
)

from .auth import get_current_user


app = FastAPI(

    title="Hospital Patient API",

    description=
        "Kasalxona patient, doctor va appointmentlarini boshqarish API",

    version="1.0.0"
)


# =====================================================
# ROUTERLAR
# =====================================================

app.include_router(
    auth.router
)

app.include_router(
    doctors.router
)

app.include_router(
    patients.router
)

app.include_router(
    appointments.router
)


# =====================================================
# BOSH SAHIFA
# =====================================================

@app.get("/")
def bosh_sahifa():

    return {

        "xabar":
            "Hospital API ishlayapti"
    }


# =====================================================
# JWT TEST
# =====================================================

@app.get(
    "/mening-profilim"
)
def mening_profilim(

    current_user =
        Depends(get_current_user)

):

    return {

        "xabar":
            "Siz autentifikatsiyadan o'tdingiz",

        "user":
            current_user
    }