from typing import List

from pydantic import BaseModel
from datetime import datetime

from schemas import Initial


class User(Initial):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class Support(Initial):
    url: str
    text: str


class Resource(Initial):
    id: int
    name: str
    year: int
    color: str
    pantone_value: str


class UserCreate(Initial):
    name: str
    job: str


class UserCreateResponse(UserCreate):
    id: int
    createdAt: datetime


class UserUpdate(UserCreate):
    pass


class UserUpdateResponse(UserCreate):
    updatedAt: datetime


class UserPatch(UserUpdate):
    pass


class UserPatchResponse(UserUpdateResponse):
    pass


class LoginForm(Initial):
    email: str
    password: str


class LoginResponseSuccess(BaseModel):
    token: str


class LoginResponseError(BaseModel):
    error: str


class RegisterForm(LoginForm):
    pass


class RegisterResponseSuccess(LoginResponseSuccess):
    id: int


class RegisterResponseError(LoginResponseError):
    pass


class UserList(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[User]
    support: Support


class UserDetail(BaseModel):
    data: User
    support: Support
