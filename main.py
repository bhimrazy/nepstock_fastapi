from typing import Optional

from fastapi import FastAPI
# others
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    return {"Hello": "World"}

@app.get("/test")
def test():
    return {"Hello": "Test"}


@app.get("/api/nepstock")
def api():
    try:
        html = urlopen('http://www.nepalstock.com')
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('The server could not be found!')
    else:
        print('It Worked!')
    bs = BeautifulSoup(html.read(), 'html.parser')
    index = bs.find('div', {'class':{'current-index'}}).text.split()[0]
    tables = bs.find_all('table', {'class':{'table table-hover table-condensed'}})[3:]
    alldata=[]
    for table in tables:
        t={}
        for row in table.find("thead").findAll('tr'):
            t["head"]=[data.text for data in row.find_all('td') if data.text !='']
            
        row_data=[]
        for row in table.find("tbody").findAll('tr'):
            col_data=[]
            for data in row.find_all('td'):
                text=data.text.split()
                if len(text) ==1 and text[0]!='' :
                    col_data.append(text[0])
                if len(text) >1:
                    col_data.append(' '.join(text))
                if len(col_data) >1:
                    row_data.append(col_data)   
            

        t["body"]=row_data 
        alldata.append(t)    
    return {
        "data": {
            "records":alldata,
            "index":index
        }
    }
