from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import router as api_router
from src.auth import router as auth_router
from src.database import engine
from sqlmodel import SQLModel

app = FastAPI(title="Secure Task Management API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header for JWT
    expose_headers=["Authorization"]
)

# Create database tables
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(api_router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure Task Management API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)