from fastapi import APIRouter

from app.api.v1.terminal import router as terminal_router

router = APIRouter(prefix="/v1")

router.include_router(terminal_router)



