from fastapi import APIRouter, HTTPException
from controller import ControllerDep
from util import Route
from pydantic import BaseModel


class RouteTypeCreate(BaseModel):
    name: str


class RouteCreate(BaseModel):
    first_end: str
    second_end: str
    route_type: str


router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("", summary="Get all routes", response_model=list[Route])
def get_all_routes(controller: ControllerDep):
    return controller.get_all_routes()


@router.post("/", summary="Add a new route")
def add_route(route: RouteCreate, controller: ControllerDep):
    try:
        controller.add_route(Route(first_end=route.first_end, second_end=route.second_end, type=route.route_type))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route added successfully."


@router.delete("/", summary="Remove a route")
def remove_route(route: RouteCreate, controller: ControllerDep):
    try:
        controller.remove_route(Route(first_end=route.first_end, second_end=route.second_end, type=route.route_type))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route removed successfully."


# Route types endpoints

@router.get("/types", summary="Get all route types, and their colors", response_model=dict[str, str])
def get_route_types(controller: ControllerDep):
    return controller.get_route_types()


@router.post("/types", summary="Add a new route type")
def add_route_type(params: RouteTypeCreate, controller: ControllerDep):
    try:
        controller.add_route_type(params.name, "")
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route type added successfully."


@router.delete("/types/", summary="Remove a route type")
def remove_route_type(params: RouteTypeCreate, controller: ControllerDep):
    try:
        controller.remove_route_type(params.name)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route type removed successfully."


@router.get("/types/all", summary="Get the name of route type that contains all of the routes.", response_model=str)
def get_route_type_all(controller: ControllerDep):
    return controller.get_route_type_all()
