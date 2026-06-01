# Middleware to time each request for measuring performance
import time
from fastapi import Request

async def timer(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-Duration"] = f"{time.perf_counter() - start:.4f}s"
    return response