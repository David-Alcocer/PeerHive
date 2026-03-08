from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    nombre: constr(strip_whitespace=True, min_length=1)
    contraseña: constr(min_length=8)
    rol: constr(strip_whitespace=True, to_lower=True) = Field(..., regex="^(admin|usuario)$")


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    nombre: Optional[constr(strip_whitespace=True, min_length=1)]
    rol: Optional[constr(strip_whitespace=True, to_lower=True)] = Field(None, regex="^(admin|usuario)$")


class UserInDB(BaseModel):
    id: str
    email: EmailStr
    nombre: str
    rol: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    nombre: str
    rol: str
