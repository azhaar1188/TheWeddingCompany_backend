from pydantic import BaseModel
from typing import Optional

class AdminLogin(BaseModel):
    email: str
    password: str


class Organization(BaseModel):
    organization_name: str
    email: str
    password: str


class OrgUpdate(BaseModel):
    new_organization_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class OrgDelete(BaseModel):
    organization_name: str
