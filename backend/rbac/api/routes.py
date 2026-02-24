from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from shared.database.session import get_db
from schemas.rbac import RoleCreate, RoleResponse, AssignRoleRequest, UserRolesResponse
from services.rbac_service import (
    get_all_roles,
    create_role,
    assign_role_to_user,
    get_user_roles_and_permissions,
)

router = APIRouter(prefix="/rbac", tags=["RBAC"])


@router.get("/roles", response_model=list[RoleResponse])
async def list_roles(db: AsyncSession = Depends(get_db)):
    return await get_all_roles(db)


@router.post("/roles", response_model=RoleResponse, status_code=201)
async def add_role(data: RoleCreate, db: AsyncSession = Depends(get_db)):
    return await create_role(db, data.name, data.description)


@router.post("/assign")
async def assign(data: AssignRoleRequest, db: AsyncSession = Depends(get_db)):
    return await assign_role_to_user(db, data.user_id, data.role_name)


@router.get("/users/{user_id}/roles", response_model=UserRolesResponse)
async def user_roles(user_id: str, db: AsyncSession = Depends(get_db)):
    return await get_user_roles_and_permissions(db, user_id)
