from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import todos, auth
from .database.connection import engine
from .models.user import User
from .models.todo import Todo
from sqlmodel import SQLModel
from dotenv import load_dotenv
from .api.error_handlers import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from starlette.exceptions import HTTPException as StarletteHTTPException
import os

load_dotenv()

app = FastAPI(title="Todo API", version="1.0.0")

# -------------------------------
# ✅ Exception Handlers
# -------------------------------
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# -------------------------------
# ✅ CORS Middleware
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# ✅ Include Routers
# -------------------------------
app.include_router(todos.router)
app.include_router(auth.router)

# -------------------------------
# ✅ Create DB Tables on Startup
# -------------------------------
@app.on_event("startup")
def on_startup():
    # This will create tables if they don't exist yet
    SQLModel.metadata.create_all(bind=engine)
    print("SUCCESS: Tables created successfully or already exist!")

# -------------------------------
# ✅ Root & Health Endpoints
# -------------------------------
@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
