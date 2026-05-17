from fastapi import APIRouter, Depends, HTTPException
from modules.ai.AICatchUpService import AIService
from depends.ai_depends import get_ai_service
from schemas.ai_schemas import CatchUpResponse


router = APIRouter(
    prefix='/ai',
    tags=['AI Integration']
)


@router.post('/task/{task_id}/catchup', response_model=CatchUpResponse)
async def get_task_catchup(
    task_id: int,
    service: AIService = Depends(get_ai_service)
):
    try:
        payload = await service.get_task_catchup_payload(task_id)

        return await service.catchup_request(payload)

    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))

    except Exception as err:
        raise HTTPException(status_code=500, detail=f'AI Service error: {str(err)}')
