from fastapi import FastAPI

from pyzer import api
from pyzer import services
from pyzer import settings

app = FastAPI()

app.include_router(api.endpoints.oauth.router)
app.include_router(api.endpoints.api.router)


@app.route("/")
async def index():
    return f"Running pyzer v{settings.VERSION}".encode()


@app.on_event("startup")
async def on_startup():
    await services.database.connect()
    await services.redis_sessions_db.initialize()


@app.on_event("shutdown")
async def on_shutdown():
    await services.database.disconnect()
    await services.redis_sessions_db.close()
