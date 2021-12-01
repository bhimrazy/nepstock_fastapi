import time
from deta import Deta
from typing import Optional
from nepstock import crawler
from pydantic import BaseModel
from fastapi import APIRouter, BackgroundTasks


router = APIRouter(
    prefix="/api",
    tags=["api"]
)

# configure your Deta project
deta = Deta("c0icbcyf_QaF3eiMteBeBrQTjPhu6GvPhoMGc13C6")
db = deta.Base('nepstock_db')


def write_data_to_db(index, datas):
    """ This function writes to deta database. """
    db.put({
        "index": index,
        "records": datas,
        "created_at": time.ctime(time.time())
    })
    print("Data Written to database")


class Item(BaseModel):
    """Item """
    name: str
    description: Optional[str] = None
    price: float


@router.get("/nepstock")
async def get_nepse_market_summary(background_tasks: BackgroundTasks):
    """This function returns scraped data"""
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
    """Returns data from database"""
    data = db.fetch()
    return data


@router.get("/test")
async def test():
    """Test """
    data: Item = {
        "name": "Hello",
        "description": "des",
        "price": "price"
    }
    return data
