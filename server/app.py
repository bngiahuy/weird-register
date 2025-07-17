from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from models import User
from database import init_db, get_db
from utils import hash_password, verify_password

app = FastAPI()
init_db()  # Khởi tạo database khi app chạy

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Đăng ký ---
@app.post("/register")
async def register(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JSONResponse(
            {"message": "Email và mật khẩu là bắt buộc"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    db = next(get_db())  # Lấy session DB

    # Kiểm tra email đã tồn tại chưa
    existing_user_email = db.query(User).filter(User.email == email).first()
    if existing_user_email:
        return JSONResponse(
            {"message": "Email này đã được sử dụng"},
            status_code=status.HTTP_409_CONFLICT,
        )

    hashed_password = hash_password(password)

    existing_user_password = (
        db.query(User).filter(User.password_hash == hashed_password).first()
    )
    
    if existing_user_password:
        return JSONResponse(
            {
                "message": f"Đây là password của {existing_user_password.email}. Hãy đổi password khác đi!"
            },
            status_code=status.HTTP_409_CONFLICT,
        )
    # --- Kết thúc logic kiểm tra mật khẩu duy nhất ---

    new_user = User(email=email, password_hash=hashed_password)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return JSONResponse(
            {"message": "Đăng ký thành công!", "user_id": new_user.id},
            status_code=status.HTTP_201_CREATED,
        )
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            {"message": "Có lỗi xảy ra khi đăng ký"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# --- Đăng nhập ---
@app.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email", "")
    password = data.get("password", "")

    if not email or not password:
        return JSONResponse(
            {"message": "Email và mật khẩu là bắt buộc"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    db = next(get_db())
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, str(user.password_hash)):
        return JSONResponse(
            {"message": "Email hoặc mật khẩu không đúng"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Ở đây bạn có thể tạo JWT token và trả về cho client
    return JSONResponse(
        {"message": "Đăng nhập thành công!", "user_id": user.id},
        status_code=status.HTTP_200_OK,
    )
