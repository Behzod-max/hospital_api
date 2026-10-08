from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

import os


# .env faylini yuklash
load_dotenv()


# =========================
# JWT SOZLAMALARI
# =========================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY .env faylida mavjud emas"
    )

ALGORITHM = "HS256"

TOKEN_AMAL_QILISH_VAQTI = 60


# =========================
# PASSWORD HASH
# =========================

parol_konteksti = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def parolni_hashlash(parol: str) -> str:
    return parol_konteksti.hash(parol)


def parolni_tekshirish(
    oddiy_parol: str,
    hash_parol: str
) -> bool:

    return parol_konteksti.verify(
        oddiy_parol,
        hash_parol
    )


# =========================
# JWT TOKEN YARATISH
# =========================

def token_yaratish(
    ma_lumotlar: dict
) -> str:

    token_malumotlari = ma_lumotlar.copy()

    tugash_vaqti = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=TOKEN_AMAL_QILISH_VAQTI
        )
    )

    token_malumotlari.update({
        "exp": tugash_vaqti
    })

    token = jwt.encode(
        token_malumotlari,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# =========================
# TOKENNI TEKSHIRISH
# =========================

def tokenni_tekshirish(
    token: str
):

    try:

        ma_lumotlar = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return ma_lumotlar

    except JWTError:

        return None


# =========================
# SWAGGER OAUTH2
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


# =========================
# CURRENT USER
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    ma_lumotlar = tokenni_tekshirish(token)

    if not ma_lumotlar:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token noto'g'ri yoki muddati tugagan",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return ma_lumotlar

def role_required(*ruxsat_etilgan_rollar):
    def tekshirish(current_user=Depends(get_current_user)):
        if current_user.get("role") not in ruxsat_etilgan_rollar:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sizda bu amalni bajarish uchun ruxsat yo'q"
            )

        return current_user

    return tekshirish