from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="ERP Invoice Service", version="1.0.0")
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "invoice"}
