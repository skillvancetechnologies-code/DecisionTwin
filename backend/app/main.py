from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    health,
    analytics,
    predict,
    datasets,
    statistics,
    simulation,
)

app = FastAPI(
    title="DecisionTwin API",
    version="1.0.0"
)

# CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(analytics.router)
app.include_router(predict.router)
app.include_router(datasets.router)
app.include_router(statistics.router)
app.include_router(simulation.router)

@app.get("/")
def root():
    return {
        "message": "DecisionTwin Backend Running"
    }