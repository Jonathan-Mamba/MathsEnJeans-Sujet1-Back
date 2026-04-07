import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import fastapi
import logging
import uvicorn
import calendar_endpoints
import game_endpoints
import player_endpoints
import route_endpoints
import square_endpoints
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from controller import ControllerDep


app = fastapi.FastAPI(redirect_slashes=False)

# Middleware order matters - add trusted hosts first
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(player_endpoints.router)
app.include_router(route_endpoints.router)
app.include_router(square_endpoints.router)  
app.include_router(calendar_endpoints.router)
app.include_router(game_endpoints.router)

@app.get("/", summary="Root Endpoint", response_model=dict)
async def root():
    return {"message": "Welcome to the Maths en Jeans Game API!", "version": "1.0.0"}

@app.get("/export", summary="Get the data of the model")
def export_data(controller: ControllerDep):
    return controller.export_model()

@app.post("/preset")
def import_(controller: ControllerDep):
    controller.import_preset()

if __name__ == "__main__":    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    port = int(os.getenv("PORT", 8000))
    logging.info(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)