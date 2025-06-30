from fastapi import APIRouter
from api.v1.auth import router as auth_router
from api.v1.events import sse_endpoint
from api.v1.telegram import router as tg_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router)
v1_router.include_router(tg_router)
v1_router.add_api_route("/events", sse_endpoint)
