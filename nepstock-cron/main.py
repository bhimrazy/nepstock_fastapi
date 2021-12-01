from fastapi import FastAPI
from utils import get_market_info,get_share_info
from deta import App


app = App(FastAPI())


@app.lib.run()
@app.get("/",tags=["Home"])
def root():
    return 'This is Cron Job API'

@app.lib.run()
@app.get("/market-info",tags=["Market"])
def get_market_data(e = None):
    return get_market_info()

@app.lib.run()
@app.get("/share-info",tags=["Share"])
def get_share_data(e = None):
    return get_share_info()

@app.lib.cron()
def cron_job(event):
    return get_market_info(upload=True)

# deta cron set "0/1 9-15 ? * 1-5 *"
    