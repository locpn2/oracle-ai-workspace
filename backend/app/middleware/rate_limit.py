from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Callable
from datetime import datetime, timedelta
import time


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests: Dict[str, list] = {}
    
    def is_rate_limited(self, key: str, max_requests: int, window_seconds: int) -> bool:
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)
        
        if key not in self.requests:
            self.requests[key] = []
        
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > window_start
        ]
        
        if len(self.requests[key]) >= max_requests:
            return True
        
        self.requests[key].append(now)
        return False
    
    def cleanup(self):
        """Remove old entries to prevent memory leak"""
        now = datetime.utcnow()
        cutoff = now - timedelta(hours=1)
        self.requests = {
            key: [t for t in times if t > cutoff]
            for key, times in self.requests.items()
        }


rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next: Callable):
    """Rate limiting middleware"""
    
    client_ip = request.client.host if request.client else "unknown"
    path = request.url.path
    
    rate_limit_config = {
        "/api/v1/auth/login": (5, 60),
        "/api/v1/auth/register": (3, 60),
    }
    
    for path_pattern, (max_requests, window) in rate_limit_config.items():
        if path.startswith(path_pattern):
            key = f"{path_pattern}:{client_ip}"
            
            if rate_limiter.is_rate_limited(key, max_requests, window):
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": f"Rate limit exceeded. Max {max_requests} requests per {window} seconds."
                    }
                )
            break
    
    response = await call_next(request)
    return response