from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.routers.api import write_data_to_db

from app.routers import api

app = FastAPI()

app.include_router(api.router)

origins = [
    "https://3000-red-hawk-mejx9fql.ws-eu15.gitpod.io",
    "https://nepstock.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/",tags=["home"])
def get_home():
    """Root Endpoint """
    return {"message": "This is NEPSTOCK API."}   

