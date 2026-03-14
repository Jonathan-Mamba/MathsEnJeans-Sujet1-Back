import fastapi
import uvicorn
import calendar_routes
import game_routes
import player_routes
import map_routes
import square_routes
from fastapi.middleware.cors import CORSMiddleware
from controller import ControllerDep
import pprint

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

@app.get("/export", summary="Get the data of the model")
def export_data(controller: ControllerDep):
    pprint.pprint(controller.export_model())
    return controller.export_model()

@app.post("/preset")
def import_(controller: ControllerDep):
    controller.import_preset()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)