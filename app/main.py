from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# settings
from app.settings import settings

# Routers
from app.routes.health import router as health_router
from app.routes.issue import router as issue_router

# Middlewares
from app.middleware.time import timer as timer_middleware

app = FastAPI(
    title='AI Jailbreak Game',
    debug=(settings.log_level.upper() == "DEBUG")
)

app.include_router(health_router)
app.include_router(issue_router)

app.middleware("http")(timer_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,            # Only allow these specific domains
    allow_credentials=True,           # Allows cookies/authentication headers
    allow_methods=["*"],              # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],              # Allows all custom headers (like Auth tokens)
)