from fastapi import FastAPI
from api.employees import router as employees_router
from api.attendance import router as attendance_router
from api.leave import router as leave_router
from api.payroll import router as payroll_router

app = FastAPI(title="ERP HRIS Service", version="1.0.0")

app.include_router(employees_router)
app.include_router(attendance_router)
app.include_router(leave_router)
app.include_router(payroll_router)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "hris"}
