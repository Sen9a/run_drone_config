from fastapi import FastAPI

from src.router import include_app_routers

app = FastAPI(description="FastAPI Drone Config upload",
              docs_url="/docs")

include_app_routers(app)