from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel, Json
from app.schemas.user import User


class ContractBase(BaseModel):
    start: Optional[date] = None
    end: Optional[date] = None


class ContractCreate(ContractBase):
    start: Optional[date] = None
    end: Optional[date] = None


class ContractUpdate(ContractBase):
    start: Optional[date] = None
    end: Optional[date] = None


class ContractDelete(ContractBase):
    id: int
    user_id: int
    start: Optional[date] = None
    end: Optional[date] = None

    class Config:
        orm_mode = True


class ContractInDBBase(ContractBase):
    id: int
    user: User
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class Contract(ContractInDBBase):
    pass


class ContractInDB(ContractInDBBase):
    pass
