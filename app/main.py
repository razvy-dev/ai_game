from fastapi import FastAPI

# Routers
from app.routes.health import router as health_router

# Middlewares
from app.middleware.time import timer as timer_middleware

app = FastAPI()

app.include_router(health_router)

app.middleware("http")(timer_middleware)