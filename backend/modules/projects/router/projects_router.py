from fastapi import APIRouter

from modules.projects.endpoints.board_api import router as board_router
from modules.projects.endpoints.column_api import router as column_router
from modules.projects.endpoints.project_api import router as project_router


router = APIRouter()
router.include_router(project_router)
router.include_router(board_router)
router.include_router(column_router)
