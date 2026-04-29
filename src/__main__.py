import fastapi
import logging
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from src.endpoints import calendar, game, player, route, square
from src.controller import ControllerDep
from src.rate_limiter import rate_limit


app = fastapi.FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(player.router)
app.include_router(route.router)
app.include_router(square.router)  
app.include_router(calendar.router)
app.include_router(game.router)

@rate_limit
@app.get("/", summary="Root Endpoint", response_model=dict)
async def root():
    return {"message": "Welcome to the Maths en Jeans Game API!", "version": "1.1.0"}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

if __name__ == "__main__":    
    print("Starting the server...")
