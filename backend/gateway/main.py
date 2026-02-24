from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.proxy import router

app = FastAPI(title="ERP API Gateway", version="1.0.0")

# CORS — allow frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "gateway"}
