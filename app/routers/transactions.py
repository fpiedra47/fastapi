from fastapi import APIRouter, HTTPException, status
from models import Transaction, TransactionCreate, Customer
from db import SessionDep
from sqlmodel import select, insert

router= APIRouter()

@router.post("/transactions", tags=["transactions"], status_code=status.HTTP_201_CREATED)

async def create_transation(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get('customer_id'))
    print(customer)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh()
    return transaction_db

@router.get("/transactions", tags=["transactions"])
async def list_transation(session: SessionDep):
    print("hgola mudo")
    query = select(Transaction)
    transactions = session.exec(query).all()
    return  transactions