from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import HTTPException
from uuid import UUID

from models.rbac import Role, Permission, user_roles, role_permissions


async def get_all_roles(db: AsyncSession):
    result = await db.execute(select(Role))
    return result.scalars().all()


async def create_role(db: AsyncSession, name: str, description: str | None) -> Role:
    existing = await db.execute(select(Role).where(Role.name == name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"Role '{name}' already exists")
    role = Role(name=name, description=description)
    db.add(role)
    await db.flush()
    return role


async def assign_role_to_user(db: AsyncSession, user_id: str, role_name: str):
    """Assign a role to a user by user_id and role name."""
    result = await db.execute(select(Role).where(Role.name == role_name))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_name}' not found")

    await db.execute(user_roles.insert().values(user_id=user_id, role_id=role.id))
    await db.flush()
    return {"message": f"Role '{role_name}' assigned to user {user_id}"}


async def get_user_roles_and_permissions(db: AsyncSession, user_id: str):
    """Get all roles and flattened permissions for a user."""
    # Get role IDs for user
    result = await db.execute(
        select(user_roles.c.role_id).where(user_roles.c.user_id == user_id)
    )
    role_ids = [row[0] for row in result.fetchall()]

    if not role_ids:
        return {"roles": [], "permissions": []}

    # Get roles with permissions
    roles_result = await db.execute(select(Role).where(Role.id.in_(role_ids)))
    roles = roles_result.scalars().all()

    role_names = [r.name for r in roles]
    permissions = set()
    for role in roles:
        for perm in role.permissions:
            permissions.add(f"{perm.resource}:{perm.action}")

    return {"roles": role_names, "permissions": list(permissions)}
