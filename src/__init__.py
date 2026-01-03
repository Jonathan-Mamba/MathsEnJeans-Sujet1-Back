import fastapi
import numpy as np
from . import calendar
from . import players
from . import routes
from . import squares

app = fastapi.FastAPI()
app.include_router(players.router)
app.include_router(routes.router)
app.include_router(squares.router)  
app.include_router(calendar.router)

@app.get("/", summary="Root Endpoint")
async def root():
    return {"message": "Welcome to the Maths en Jeans Game API!", "version": "1.0"}