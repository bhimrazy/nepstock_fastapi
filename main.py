from typing import Optional

from fastapi import FastAPI
# others
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


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
        "data": alldata
    }
