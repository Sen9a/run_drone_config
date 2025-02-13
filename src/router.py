from src.api.drone_config import router as drone_config_router

def include_app_routers(app):
    app.include_router(drone_config_router)