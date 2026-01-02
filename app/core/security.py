from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _prehash_password(passwd: str) -> str:
    """
    Pre-hash con SHA256 para evitar límite de 72 bytes de bcrypt.
    """
    return hashlib.sha256(passwd.encode("utf-8")).hexdigest()

def hash_password(passwd: str) -> str:
    prehashed = _prehash_password(passwd)
    return pwd_context.hash(prehashed)

def verificar_password(passwd: str, hashed: str) -> bool:
    prehashed = _prehash_password(passwd)
    return pwd_context.verify(prehashed, hashed)
