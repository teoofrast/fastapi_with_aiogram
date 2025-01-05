import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.user_route import router as user_router
from routes.service_route import router as service_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(user_router)
app.include_router(service_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )