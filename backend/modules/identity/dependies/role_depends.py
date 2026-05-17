from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from modules.identity.repos.user_repository import RoleRepository
from modules.identity.services.role_service import RoleService


def get_role_repository(session: AsyncSession = Depends(get_db)) -> RoleRepository:
    return RoleRepository(session)


def get_role_service(
    role_repo: RoleRepository = Depends(get_role_repository),
) -> RoleService:
    return RoleService(role_repo)
