"""Health check with build SHA, per smoke-test #1."""
import os

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "build_sha": os.getenv("BUILD_SHA", "dev"),
    }
