import os

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
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from controller import ControllerDep


class StrippedTrailingSlashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path != "/" and request.url.path.endswith("/"):
            request.scope["path"] = request.url.path.rstrip("/")
        return await call_next(request)


app = fastapi.FastAPI(redirect_slashes=False)

# Middleware order matters - add trusted hosts first
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(StrippedTrailingSlashMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
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

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))