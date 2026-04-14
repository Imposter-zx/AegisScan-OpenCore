"""
Authentication module for AegisScan Strategic v4.0 REST API
Provides JWT-based authentication and API key validation
"""

import os
import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from functools import wraps
from flask import request, jsonify, g

# In a production environment, these would be stored securely
# For Open-Core, we use environment variables or config files
SECRET_KEY = os.environ.get("AEGISCAN_API_SECRET", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Mock user database (in production, use a real database)
MOCK_USERS = {
    "admin": {
        "username": "admin",
        "hashed_password": bcrypt.hashpw(
            "admin123".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8"),
        "role": "admin",
        "permissions": ["scan:read", "scan:write", "admin:all"],
    },
    "operator": {
        "username": "operator",
        "hashed_password": bcrypt.hashpw(
            "operator123".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8"),
        "role": "operator",
        "permissions": ["scan:read", "scan:write"],
    },
    "viewer": {
        "username": "viewer",
        "hashed_password": bcrypt.hashpw(
            "viewer123".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8"),
        "role": "viewer",
        "permissions": ["scan:read"],
    },
}


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None


def get_current_user() -> Optional[Dict[str, Any]]:
    """Get the current authenticated user from request context"""
    return getattr(g, "current_user", None)


def require_auth(permission: str = None):
    """Decorator to require authentication and optionally a specific permission"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check for Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"error": "Authorization header required"}), 401

            # Extract token
            try:
                token_type, token = auth_header.split(" ")
                if token_type.lower() != "bearer":
                    return jsonify(
                        {"error": "Invalid authorization type. Use Bearer token"}
                    ), 401
            except ValueError:
                return jsonify({"error": "Invalid authorization header format"}), 401

            # Verify token
            payload = verify_token(token)
            if not payload:
                return jsonify({"error": "Invalid or expired token"}), 401

            # Get user info
            username = payload.get("sub")
            if not username or username not in MOCK_USERS:
                return jsonify({"error": "User not found"}), 401

            user = MOCK_USERS[username]

            # Check permissions if required
            if permission:
                user_permissions = user.get("permissions", [])
                if (
                    permission not in user_permissions
                    and "admin:all" not in user_permissions
                ):
                    return jsonify({"error": "Insufficient permissions"}), 403

            # Store user in request context
            g.current_user = user
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def optional_auth(f):
    """Decorator for optional authentication"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token_type, token = auth_header.split(" ")
                if token_type.lower() == "bearer":
                    payload = verify_token(token)
                    if payload:
                        username = payload.get("sub")
                        if username and username in MOCK_USERS:
                            g.current_user = MOCK_USERS[username]
            except (ValueError, AttributeError):
                pass  # Ignore invalid tokens for optional auth
        return f(*args, **kwargs)

    return decorated_function


def generate_api_key() -> str:
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)


def validate_api_key(api_key: str) -> bool:
    """Validate an API key (would check against database in production)"""
    # For Open-Core, we'll accept any properly formatted key
    # In production, this would check against a stored list
    return len(api_key) >= 32


# Initialize some default users if needed
def init_auth():
    """Initialize authentication system"""
    # In a real implementation, this would load users from database/config
    # For Open-Core, our mock users are already defined above
    pass


__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "verify_token",
    "get_current_user",
    "require_auth",
    "optional_auth",
    "generate_api_key",
    "validate_api_key",
    "init_auth",
    "SECRET_KEY",
    "ALGORITHM",
]
