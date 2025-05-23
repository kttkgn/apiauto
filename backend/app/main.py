from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router

app = FastAPI(
    title="接口自动化平台",
    description="一个轻量、高效、可扩展的接口自动化测试平台",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载API路由
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to API Automation Platform"} 