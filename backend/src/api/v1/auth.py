from fastapi import APIRouter, HTTPException, Path, status

router = APIRouter(prefix="/auth")


@router.post("/signin")
async def signin(): ...
