from fastapi import APIRouter

from . import v2

router = APIRouter(prefix="/api")

router.include_router(v2.router)
