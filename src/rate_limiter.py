from asyncio import get_event_loop
from functools import wraps
from fastapi import HTTPException, Request
from typing import Callable, Any

# Global dict to track request counts: {ip: [timestamp, timestamp, ...]}
request_tracker: dict[str, list[float]] = {}

# Rate limit configuration
REQUESTS_PER_MINUTE = 100
TIME_WINDOW = 60  # seconds


def rate_limit(func: Callable) -> Callable:
    """
    Decorator to rate limit endpoints based on client IP address.
    Limits to REQUESTS_PER_MINUTE requests per TIME_WINDOW seconds.
    """
    @wraps(func)
    async def async_wrapper(request: Request, *args, **kwargs) -> Any:
        client_ip = request.client.host if request.client else "unknown"
        current_time = get_event_loop().time()
        
        # Initialize or get the request history for this IP
        if client_ip not in request_tracker:
            request_tracker[client_ip] = []
        
        # Remove old requests outside the time window
        request_tracker[client_ip] = [
            timestamp for timestamp in request_tracker[client_ip]
            if current_time - timestamp < TIME_WINDOW
        ]
        
        # Check if limit exceeded
        if len(request_tracker[client_ip]) >= REQUESTS_PER_MINUTE:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {REQUESTS_PER_MINUTE} requests per {TIME_WINDOW} seconds."
            )
        
        # Add current request
        request_tracker[client_ip].append(current_time)
        
        # Call the original function
        return await func(*args, **kwargs)
    return async_wrapper