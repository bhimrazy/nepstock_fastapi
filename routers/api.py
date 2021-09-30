from fastapi import APIRouter, BackgroundTasks
from typing import Optional
from deta import Deta
from nepstock import crawler
from pydantic import BaseModel
import time

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

deta = Deta("c0icbcyf_QaF3eiMteBeBrQTjPhu6GvPhoMGc13C6")  # configure your Deta project
db = deta.Base('nepstock_db')

def write_data_to_db(index, datas):
    """ This function writes to deta database. """
    db.put({
        "index": index,
        "records": datas,
        "created_at":time.ctime(time.time())
    })
    print("Data Written to database")


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    

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

@router.get("/test")
async def test():
    data:Item = {
        "name":"Hello",
        "description":"des",
        "price":"price"
    }
    return data