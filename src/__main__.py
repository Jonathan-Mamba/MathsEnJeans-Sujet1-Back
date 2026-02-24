import fastapi
import uvicorn
import src.calendar_routes as calendar_routes, src.game_routes as game_routes, map_routes, src.player_routes as player_routes, src.square_routes as square_routes
from fastapi.middleware.cors import CORSMiddleware
from controller import ControllerDep
import util

app = fastapi.FastAPI()
app.include_router(player_routes.router)
app.include_router(map_routes.router)
app.include_router(square_routes.router)  
app.include_router(calendar_routes.router)
app.include_router(game_routes.router)

origins = [
    "http://localhost:5173",
    "http://localhost:*",
    "https://localhost:*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="Root Endpoint", response_model=dict)
async def root():
    return {"message": "Welcome to the Maths en Jeans Game API!", "version": "1.0"}

@app.get("/export", summary="Get the data of the model", response_model=util.ExportDict)
def export_data(controller: ControllerDep):
    return controller.export_model()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)