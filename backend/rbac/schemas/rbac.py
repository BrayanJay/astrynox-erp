from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class PermissionResponse(BaseModel):
    id: UUID
    resource: str
    action: str
    description: str | None
    class Config:
        from_attributes = True


class RoleResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    permissions: list[PermissionResponse]
    created_at: datetime
    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class AssignRoleRequest(BaseModel):
    user_id: str
    role_name: str


class UserRolesResponse(BaseModel):
    roles: list[str]
    permissions: list[str]
