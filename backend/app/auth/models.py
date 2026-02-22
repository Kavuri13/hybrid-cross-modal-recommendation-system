"""
User database models and schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import json
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


# --- Request Models ---

class UserRegister(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: str = Field(..., min_length=2, description="Full name")


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    """Forgot password request"""
    email: EmailStr


# --- Response Models ---

class UserResponse(BaseModel):
    """User response (without password)"""
    user_id: str
    email: str
    full_name: str
    created_at: datetime
    is_active: bool = True


class TokenResponse(BaseModel):
    """Authentication token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# --- Database Models ---

class User:
    """User database model with JSON file storage"""
    def __init__(self, user_id: str, email: str, full_name: str, hashed_password: str):
        self.user_id = user_id
        self.email = email
        self.full_name = full_name
        self.hashed_password = hashed_password
        self.created_at = datetime.utcnow()
        self.is_active = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary (excluding password)"""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "is_active": self.is_active
        }
    
    def to_dict_with_password(self) -> dict:
        """Convert to dictionary including hashed password for storage"""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "full_name": self.full_name,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "is_active": self.is_active
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Create User from dictionary"""
        user = User(data["user_id"], data["email"], data["full_name"], data["hashed_password"])
        if isinstance(data["created_at"], str):
            user.created_at = datetime.fromisoformat(data["created_at"])
        else:
            user.created_at = data["created_at"]
        user.is_active = data.get("is_active", True)
        return user


# --- JSON File Storage ---

class JSONUserStore:
    """JSON-based user storage"""
    
    def __init__(self):
        # Get data directory
        repo_root = None
        for parent in [Path(__file__).resolve()] + list(Path(__file__).resolve().parents):
            if (parent / "data").exists():
                repo_root = parent
                break
        
        if repo_root is None:
            repo_root = Path(__file__).resolve().parents[3]  # backend/app/auth -> project root
        
        self.data_dir = repo_root / "data"
        self.users_file = self.data_dir / "users.json"
        
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize JSON file if it doesn't exist
        if not self.users_file.exists():
            self._initialize_file()
        
        logger.info(f"User storage initialized at: {self.users_file}")
    
    def _initialize_file(self):
        """Initialize empty users JSON file"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump({"users": []}, f, indent=2, ensure_ascii=False)
    
    def _load_users(self) -> dict:
        """Load all users from JSON file"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {user["email"]: User.from_dict(user) for user in data.get("users", [])}
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            return {}
    
    def _save_users(self, users: dict):
        """Save all users to JSON file"""
        try:
            users_list = [user.to_dict_with_password() for user in users.values()]
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump({"users": users_list}, f, indent=2, ensure_ascii=False)
            logger.info(f"Users saved to {self.users_file}")
        except Exception as e:
            logger.error(f"Error saving users: {e}")
            raise
    
    def create_user(self, email: str, password: str, full_name: str) -> User:
        """Create a new user"""
        from app.auth.utils import get_password_hash
        import uuid
        
        users = self._load_users()
        
        if email in users:
            raise ValueError("User with this email already exists")
        
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(password)
        user = User(user_id, email, full_name, hashed_password)
        
        users[email] = user
        self._save_users(users)
        
        logger.info(f"New user created: {email}")
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        users = self._load_users()
        return users.get(email)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        from app.auth.utils import verify_password
        
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def user_exists(self, email: str) -> bool:
        """Check if user exists"""
        users = self._load_users()
        return email in users


# --- Global store instance ---
user_store = JSONUserStore()


# --- Convenience functions ---

def create_user(email: str, password: str, full_name: str) -> User:
    """Create a new user"""
    return user_store.create_user(email, password, full_name)


def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email"""
    return user_store.get_user_by_email(email)


def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    return user_store.authenticate_user(email, password)
