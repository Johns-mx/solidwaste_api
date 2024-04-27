from datetime import datetime
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass
class VersionAPI():
    major= 1
    minor= 0
    patch= 0
    version: str = f"v{major}.{minor}.{patch}"


@dataclass
class UserInternalData:
    user_id: Optional[int]= None
    username: Optional[str]= None
    email: Optional[str]= None
    full_name: Optional[str]= None
    is_owner: Optional[bool]= None
    owner_id: Optional[str]= None
    is_active: Optional[bool]= None
    is_admin: Optional[bool]= False


@dataclass
class KeyUserInternalData:
    key_id: Optional[int]= None
    user_id: Optional[int]= None
    owner_id: Optional[str]= None
    created_at: Optional[str | datetime]= None

@dataclass
class KeyUserData:
    key_id: Optional[int]= None
    user_id: Optional[int]= None
    owner_id: Optional[str]= None


class ResponseModel(BaseModel):
    status: int= 400
    error: bool= True
    message: str= ""
    res: Optional[Any] = None
    version: Optional[str]= VersionAPI().version


class KeyUser(BaseModel):
    """[model] Plantilla: KeyUser"""
    user_token: str


class UserModel(BaseModel):
    """Modelo completo de la tabla User"""
    user_id: Optional[int]= None
    username: Optional[str]= None
    password: Optional[str]= None
    email: Optional[str]= None
    full_name: Optional[str]= None
    is_owner: Optional[bool]= True
    owner_id: Optional[str]= None
    created_at: Optional[str | datetime]= None
    updated_at: Optional[str | datetime]= None
    is_active: Optional[bool]= None
    phone: Optional[str]= None
    language: Optional[str]= None
    id_card: Optional[str]= None
    is_admin: Optional[bool]= None


class SubUserModel(BaseModel):
    """Modelo completo de la tabla SubUser"""
    user_id: Optional[int]= None
    owner_id: Optional[str]= None
    username: Optional[str]= None
    password: Optional[str]= None
    email: Optional[str]= None
    full_name: Optional[str]= None
    is_owner: Optional[bool]= False
    is_active: Optional[bool]= None


class KeyUserModel(BaseModel):
    """Modelo completo de la tabla KeyUser"""
    key_id: Optional[int]= None
    user_id: Optional[int]= None
    owner_id: Optional[int]= None
    keyuser: Optional[str]= None
    created_at: Optional[str | datetime]= None


class TownHallModel(BaseModel):
    """Modelo completo de la tabla TownHall"""
    id: Optional[int]= None
    title: Optional[str]= None
    description: Optional[str]= None
    community: Optional[str]= None
    location: Optional[Dict[str, Any]]= None
    contacts: Optional[Dict[str, Any]]= None
    is_active: Optional[bool]= None
    is_available: Optional[bool]= None
    created_at: Optional[str | datetime]= None
    updated_at: Optional[str | datetime]= None


class UserCreate(BaseModel):
    """[model] Plantilla: User"""
    username: str
    password: str
    email: str
    full_name: str


class SubUserCreate(UserCreate):
    """[model] Plantilla: Sub User"""
    user_token: str

class ContactsTownHall(BaseModel):
    link: Optional[str]= None
    fax: Optional[str]= None
    tel: Optional[str]= None

class LocationTownHall(BaseModel):
    lat: Optional[str]= None
    lng: Optional[str]= None
    address: Optional[str]= None

class TownHallCreate(KeyUser):
    """[model] Plantilla: TownHall"""
    title: str
    description: str
    community: str
    location: Optional[LocationTownHall]= None
    contacts: Optional[ContactsTownHall]= None
    email: str

class UserInternalModel(BaseModel):
    username: Optional[str]= None
    password: Optional[str]= None
    email: Optional[str]= None
    full_name: Optional[str]= None
    owner_id: Optional[str]= None


class SubUserInternalModel(BaseModel):
    owner_id: Optional[str]= None
    username: Optional[str]= None
    password: Optional[str]= None
    email: Optional[str]= None
    full_name: Optional[str]= None


class TownHallInternalModel(KeyUser):
    title: Optional[str]= None
    description: Optional[str]= None
    community: Optional[str]= None
    location: Optional[Dict[str, Any]]= None
    contacts: Optional[Dict[str, Any]]= None
    email: Optional[str]= None
    is_active: Optional[bool]= None
    is_available: Optional[bool]= None


class SubKeyUser(KeyUser):
    """[model] Plantilla: SubKeyUser"""
    username: str

class UserSignIn(BaseModel):
    """[model] Plantilla: UserSignIn"""
    username_or_email: str
    password: str

class UserSignOut(BaseModel):
    """[model] Plantilla: UserSignOut"""
    user_token: str


class UserUpdateInternal(BaseModel):
    full_name: Optional[str]= None