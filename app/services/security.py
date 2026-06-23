import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Optional

from app.config import settings

_PBKDF2_ITERATIONS = 100_000


def generate_salt() -> str:
    return secrets.token_hex(16)


def hash_password(password: str, salt: str) -> str:
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), _PBKDF2_ITERATIONS
    )
    return derived.hex()


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    candidate = hash_password(password, salt)
    return hmac.compare_digest(candidate, expected_hash)


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _sign(payload_b64: str) -> str:
    signature = hmac.new(
        settings.secret_key.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256
    ).digest()
    return _b64encode(signature)


def create_token(user_id: str, now: Optional[int] = None) -> str:
    """Create an HMAC-signed token carrying the user id and an expiry timestamp."""
    issued = int(now if now is not None else time.time())
    payload = {"uid": user_id, "exp": issued + settings.token_ttl_minutes * 60}
    payload_b64 = _b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    return f"{payload_b64}.{_sign(payload_b64)}"


def verify_token(token: str, now: Optional[int] = None) -> str:
    """Return the user id for a valid, unexpired token, else raise ValueError."""
    try:
        payload_b64, signature = token.split(".", 1)
    except ValueError:
        raise ValueError("Malformed token")

    if not hmac.compare_digest(signature, _sign(payload_b64)):
        raise ValueError("Invalid token signature")

    payload = json.loads(_b64decode(payload_b64).decode("utf-8"))
    current = int(now if now is not None else time.time())
    if current >= int(payload.get("exp", 0)):
        raise ValueError("Token expired")

    return str(payload["uid"])
