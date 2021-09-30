from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.nepstock import crawler
# from app.routers.api import write_data_to_db
# from deta import App
from app.routers import api

# app = App(FastAPI())
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


@app.get("/")
def read_root():
    """Root Endpoint """
    return {"message": "Hello World"}


# @app.lib.cron()
# def cron_job(event):
#     alldata, index = crawler.crawler()
#     write_data_to_db(index, alldata)
#     return f"Data Written Successfully with index: {index} "
# deta cron set "0/1 9-15 ? * 1-5 *"
