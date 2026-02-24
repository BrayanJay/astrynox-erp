import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from shared.database.session import Base

# Association table: role <-> permission (many-to-many)
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("rbac.roles.id"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("rbac.permissions.id"), primary_key=True),
    schema="rbac",
)

# Association table: user <-> role (many-to-many)
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), primary_key=True),
    Column("role_id", UUID(as_uuid=True), ForeignKey("rbac.roles.id"), primary_key=True),
    schema="rbac",
)


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "rbac"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles", lazy="selectin")


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "rbac"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource = Column(String(100), nullable=False)   # e.g. "quotation", "hris"
    action = Column(String(100), nullable=False)      # e.g. "create", "view_employees"
    description = Column(String(255))

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions", lazy="selectin")
