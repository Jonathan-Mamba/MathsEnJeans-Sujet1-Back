import fastapi
import numpy as np
from . import calendar
from . import players
from . import routes
from . import squares
from . import game
from fastapi.middleware.cors import CORSMiddleware


app = fastapi.FastAPI()
app.include_router(players.router)
app.include_router(routes.router)
app.include_router(squares.router)  
app.include_router(calendar.router)
app.include_router(game.router)

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="Root Endpoint")
async def root():
    return {"message": "Welcome to the Maths en Jeans Game API!", "version": "1.0"}