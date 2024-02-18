from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api_v1 import router as router_v1


app = FastAPI(docs_url="/api/docs", debug=True, title="FastAPI TaskControlSystem")

app.include_router(router_v1, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
