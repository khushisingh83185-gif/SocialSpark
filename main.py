from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import engine, Base
from app.routes import data

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SocialSpark API",
    description="Backend API for Social Media Engagement Analytics & Prediction System",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(data.router)

@app.get("/")
def root():
    return {"message": "Welcome to SocialSpark API!"}
