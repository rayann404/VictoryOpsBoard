from fastapi import APIRouter

from backend.modules.tasks.endpoints.activities.task_activity_api import router as activity_router
from backend.modules.tasks.endpoints.comments.comment_api import router as comment_router
from backend.modules.tasks.endpoints.tasks.task_api import router as task_router


router = APIRouter()
router.include_router(task_router)
router.include_router(comment_router)
router.include_router(activity_router)
