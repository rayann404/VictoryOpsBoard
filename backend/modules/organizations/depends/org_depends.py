from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from modules.organizations.repo.repository import OrganizationRepository
from modules.organizations.service.org_service import OrganizationService


def get_organization_repository(
    session: AsyncSession = Depends(get_db),
) -> OrganizationRepository:
    return OrganizationRepository(session)


def get_organization_service(
    repository: OrganizationRepository = Depends(get_organization_repository),
) -> OrganizationService:
    return OrganizationService(repository)
