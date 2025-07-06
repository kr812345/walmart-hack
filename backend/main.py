from fastapi import FastAPI
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
@app.get("/")
async def root():
    print ("Health check endpoint hit")
    return {"message": "LiveExpiry+ Backend is Running"}
