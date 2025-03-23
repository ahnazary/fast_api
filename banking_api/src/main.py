import uvicorn
from fastapi import FastAPI
from postgres_interface import Base, create_tables, engine, fill_tables
from routes import accounts, auth, customers, transactions, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking API",
    description="An internal banking API for managing accounts and transactions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


@app.get("/", tags=["Health Check"])
def health_check():
    return {"message": "Banking API is running ..."}


if __name__ == "__main__":
    # We create the tables and fill them with some data to begin with
    create_tables()
    fill_tables()
    uvicorn.run(app, port=8000, host="0.0.0.0")
