"""
FastAPI 앱 진입점
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import endpoints

# FastAPI 앱 생성
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: 운영 환경에서는 구체적인 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: 라우터 등록
# app.include_router(endpoints.health.router)
# app.include_router(endpoints.chat.router)
# app.include_router(endpoints.workshop.router)


@app.get("/")
async def root():
    """
    루트 엔드포인트
    """
    return {"message": "SKouter AI Backend"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
