from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    hashed = pwd_context.hash(password, salt="2222222222222222222222")
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    print("Verifying password:", plain_password)    
    return pwd_context.verify(plain_password, hashed_password)