from fastapi import FastAPI
from backend.routers import simulation
from backend.routers import inventory
from backend.routers import recommendation
from backend.routers import co2
# from fastapi.middleware.cors import CORSMiddleware
# from api.endpoints import router as api_router

app = FastAPI(title="LiveExpiry+ Backend")

# CORS Setup
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Open for all during hackathon
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Register API Routes
# app.include_router(api_router)

# Health Check Endpoint

app.include_router(simulation.router)
app.include_router(inventory.router)
app.include_router(recommendation.router)
app.include_router(co2.router)


@app.get("/")
async def root():
    print ("Health check endpoint hit")
    return {"message": "LiveExpiry+ Backend is Running"}
