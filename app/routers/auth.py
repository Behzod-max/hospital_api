from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User

from ..schemas import (
    UserRoyxatdanOtish,
    UserJavob,
    LoginSchema
)

from ..auth import (
    parolni_hashlash,
    parolni_tekshirish,
    token_yaratish
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =====================================================
# REGISTER
# =====================================================

@router.post(
    "/register",
    response_model=UserJavob,
    status_code=status.HTTP_201_CREATED
)
def royxatdan_otish(
    foydalanuvchi: UserRoyxatdanOtish,
    db: Session = Depends(get_db)
):

    # Username tekshirish

    mavjud_username = db.query(User).filter(
        User.username == foydalanuvchi.username
    ).first()

    if mavjud_username:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu username allaqachon mavjud"
        )


    # Email tekshirish

    mavjud_email = db.query(User).filter(
        User.email == foydalanuvchi.email
    ).first()

    if mavjud_email:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email allaqachon mavjud"
        )


    # Parolni hash qilish

    hash_parol = parolni_hashlash(
        foydalanuvchi.password
    )


    # User yaratish

    yangi_foydalanuvchi = User(

        username=foydalanuvchi.username,

        email=foydalanuvchi.email,

        password=hash_parol,

        role="patient"
    )


    db.add(
        yangi_foydalanuvchi
    )

    db.commit()

    db.refresh(
        yangi_foydalanuvchi
    )


    return yangi_foydalanuvchi


# =====================================================
# LOGIN — JSON
# =====================================================

@router.post(
    "/login"
)
def login(
    foydalanuvchi: LoginSchema,
    db: Session = Depends(get_db)
):

    mavjud_foydalanuvchi = db.query(User).filter(
        User.username == foydalanuvchi.username
    ).first()


    if not mavjud_foydalanuvchi:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username yoki parol noto'g'ri"
        )


    parol_togri = parolni_tekshirish(

        foydalanuvchi.password,

        mavjud_foydalanuvchi.password
    )


    if not parol_togri:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username yoki parol noto'g'ri"
        )


    token = token_yaratish({

        "sub": str(
            mavjud_foydalanuvchi.id
        ),

        "username":
            mavjud_foydalanuvchi.username,

        "role":
            mavjud_foydalanuvchi.role
    })


    return {

        "access_token": token,

        "token_type": "bearer"
    }


# =====================================================
# TOKEN — SWAGGER UCHUN
# =====================================================

@router.post(
    "/token"
)
def token_olish(

    form_data:
        OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)
):

    # Username orqali user topish

    foydalanuvchi = db.query(User).filter(

        User.username ==
        form_data.username

    ).first()


    if not foydalanuvchi:

        raise HTTPException(

            status_code=
                status.HTTP_401_UNAUTHORIZED,

            detail=
                "Username yoki parol noto'g'ri"
        )


    # Parolni tekshirish

    parol_togri = parolni_tekshirish(

        form_data.password,

        foydalanuvchi.password
    )


    if not parol_togri:

        raise HTTPException(

            status_code=
                status.HTTP_401_UNAUTHORIZED,

            detail=
                "Username yoki parol noto'g'ri"
        )


    # JWT yaratish

    token = token_yaratish({

        "sub":
            str(foydalanuvchi.id),

        "username":
            foydalanuvchi.username,

        "role":
            foydalanuvchi.role
    })


    # OAuth2 talab qiladigan format

    return {

        "access_token": token,

        "token_type": "bearer"
    }