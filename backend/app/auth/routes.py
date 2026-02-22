"""
Authentication routes for user registration, login, and management
"""
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
import logging

from app.auth.models import (
    UserRegister, UserLogin, TokenResponse, UserResponse,
    ForgotPasswordRequest, create_user, get_user_by_email, authenticate_user
)
from app.auth.utils import (
    create_access_token, get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user
    
    - Creates new user account
    - Returns access token
    """
    try:
        # Check if user already exists
        existing_user = get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create new user
        user = create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.user_id},
            expires_delta=access_token_expires
        )
        
        logger.info(f"New user registered: {user.email}")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(**user.to_dict())
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@auth_router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """
    Login user
    
    - Authenticates user credentials
    - Returns access token
    """
    # Authenticate user
    user = authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.user_id},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {user.email}")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(**user.to_dict())
    )


@auth_router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information
    
    - Requires authentication
    - Returns user profile
    """
    user = get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(**user.to_dict())


@auth_router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """
    Request password reset
    
    - Takes email address
    - In production: sends reset email with token
    - Returns success if email exists
    """
    try:
        user = get_user_by_email(request.email)
        if not user:
            # For security, we don't reveal if email exists
            # But return success anyway
            logger.warning(f"Password reset requested for non-existent email: {request.email}")
        else:
            logger.info(f"Password reset requested for: {request.email}")
        
        return {
            "message": f"If an account exists with {request.email}, a password reset link has been sent to that email."
        }
    except Exception as e:
        logger.error(f"Error processing forgot password request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing your request"
        )


@auth_router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout user
    
    - Requires authentication
    - Client should discard the token
    """
    logger.info(f"User logged out: {current_user['email']}")
    return {"message": "Successfully logged out"}
