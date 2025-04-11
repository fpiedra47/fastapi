import zoneinfo
import time
from datetime import datetime
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Request 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import  Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select
from .routers import customers, transactions, plans

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in: {process_time:.4f} seconds")
    return response

security = HTTPBasic() 

@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    print(credentials)
    return {"message": "Hola, Fer!"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

@app.get("/time/{iso_code}")
async def get_time_by_iso_code(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

@app.post("/invoices", response_model=Invoice)
async def create_invoice(invoice_data: Invoice):
    breakpoint()
    return invoice_data