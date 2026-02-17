from fastapi import APIRouter, HTTPException
from src.controller import ControllerDep
from src.datatypes import Route, Square, RouteType

router = APIRouter(prefix="/routes", tags=["routes"])

@router.get("/", summary="Get all routes", response_model=list[Route])
def get_all_routes(controller: ControllerDep):
    return controller.get_all_routes()

@router.get("/types", summary="Get all route types, and their colors", response_model=dict[RouteType, str])
def get_route_types(controller: ControllerDep):
    return controller.get_route_types()

@router.post("/", summary="Add a new route")
def add_route(first_end: Square, second_end: Square, route_type: RouteType, controller: ControllerDep):
    try:
        controller.add_route(Route(first_end=first_end, second_end=second_end, type=route_type))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route added successfully."

@router.delete("/", summary="Remove a route")
def remove_route(first_end: Square, second_end: Square, route_type: RouteType, controller: ControllerDep):
    try:
        controller.remove_route(Route(first_end=first_end, second_end=second_end, type=route_type))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route removed successfully."
