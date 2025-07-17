from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from models import User
from database import init_db, get_db
from utils import hash_password, verify_password

app = FastAPI()
init_db()  # Initialize database when app starts

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Register ---
@app.post("/register")
async def register(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JSONResponse(
            {"message": "Email and password are required"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    db = next(get_db())  # Get DB session

    # Check if email already exists
    existing_user_email = db.query(User).filter(User.email == email).first()
    if existing_user_email:
        return JSONResponse(
            {"message": "This email is already in use"},
            status_code=status.HTTP_409_CONFLICT,
        )

    hashed_password = hash_password(password)

    existing_user_password = (
        db.query(User).filter(User.password_hash == hashed_password).first()
    )

    if existing_user_password:
        return JSONResponse(
            {
                "message": f"This is the password of {existing_user_password.email}. Please choose a different password!"
            },
            status_code=status.HTTP_409_CONFLICT,
        )
    # --- End unique password check logic ---

    new_user = User(email=email, password_hash=hashed_password)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return JSONResponse(
            {"message": "Registration successful!", "user_id": new_user.id},
            status_code=status.HTTP_201_CREATED,
        )
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            {"message": "An error occurred during registration"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# --- Login ---
@app.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email", "")
    password = data.get("password", "")

    if not email or not password:
        return JSONResponse(
            {"message": "Email and password are required"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    db = next(get_db())
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, str(user.password_hash)):
        return JSONResponse(
            {"message": "Incorrect email or password"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Here you can create a JWT token and return it to the client
    return JSONResponse(
        {"message": "Login successful!", "user_id": user.id},
        status_code=status.HTTP_200_OK,
    )
