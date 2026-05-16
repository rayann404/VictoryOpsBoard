from fastapi import APIRouter

from backend.modules.projects.endpoints.boards.board_api import router as board_router
from backend.modules.projects.endpoints.columns.column_api import router as column_router
from backend.modules.projects.endpoints.projects.project_api import router as project_router


router = APIRouter()
router.include_router(project_router)
router.include_router(board_router)
router.include_router(column_router)
