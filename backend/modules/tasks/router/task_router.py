from fastapi import APIRouter

from modules.tasks.endpoints.comment_api import router as comment_router
from modules.tasks.endpoints.task_activity_api import router as activity_router
from modules.tasks.endpoints.task_api import router as task_router


router = APIRouter()
router.include_router(task_router)
router.include_router(comment_router)
router.include_router(activity_router)
