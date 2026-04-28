from fastapi import APIRouter, HTTPException, Request
from src.controller import ControllerDep
from src.util import Route
from pydantic import BaseModel
from src.rate_limiter import rate_limit


class RouteTypeCreate(BaseModel):
    name: str


class RouteCreate(BaseModel):
    first_end: str
    second_end: str
    route_type: str


router = APIRouter(prefix="/routes", tags=["routes"])


@rate_limit
@router.get("/", summary="Get all routes", response_model=list[Route])
def get_all_routes(request: Request, controller: ControllerDep):
    return controller.get_all_routes()


@rate_limit
@router.post("/", summary="Add a new route")
def add_route(request: Request, route: RouteCreate, controller: ControllerDep):
    try:
        controller.add_route(Route(first_end=route.first_end, second_end=route.second_end, type=route.route_type))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route added successfully."


@rate_limit
@router.delete("/", summary="Remove a route")
def remove_route(request: Request, route: RouteCreate, controller: ControllerDep):
    try:
        controller.remove_route(Route(first_end=route.first_end, second_end=route.second_end, type=route.route_type))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route removed successfully."


# Route types endpoints

@rate_limit
@router.get("/types", summary="Get all route types, and their colors", response_model=dict[str, str])
def get_route_types(request: Request, controller: ControllerDep):
    return controller.get_route_types()


@rate_limit
@router.post("/types", summary="Add a new route type")
def add_route_type(request: Request, params: RouteTypeCreate, controller: ControllerDep):
    try:
        controller.add_route_type(params.name, "")
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route type added successfully."


@rate_limit
@router.delete("/types/", summary="Remove a route type")
def remove_route_type(request: Request, params: RouteTypeCreate, controller: ControllerDep):
    try:
        controller.remove_route_type(params.name)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Route type removed successfully."


@rate_limit
@router.get("/types/all", summary="Get the name of route type that contains all of the routes.", response_model=str)
def get_route_type_all(request: Request, controller: ControllerDep):
    return controller.get_route_type_all()
