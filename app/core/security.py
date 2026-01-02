from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(passwd: str) -> str:
    return pwd_context.hash(passwd)

def verificar_password(passwd: str, hashed: str) -> bool:
    return pwd_context.verify(passwd, hashed)
