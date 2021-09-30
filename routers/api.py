from fastapi import APIRouter, BackgroundTasks
from deta import Deta
from nepstock import crawler
import time

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

deta = Deta("c0icbcyf_QaF3eiMteBeBrQTjPhu6GvPhoMGc13C6")  # configure your Deta project
db = deta.Base('nepstock_db')

def write_data_to_db(index, alldata):
    db.put({
        "index": index,
        "records": alldata,
        "created_at":time.ctime(time.time())
    })
    print("Data Written to database")


@router.get("/nepstock")
async def nepstock(background_tasks: BackgroundTasks):
    alldata, index = crawler.crawler()
    background_tasks.add_task(write_data_to_db, index, alldata)
    return {
        "data": {
            "index": index,
            "records": alldata
        }
    }

@router.get("/db")
async def database():
    data= db.fetch()
    return data
