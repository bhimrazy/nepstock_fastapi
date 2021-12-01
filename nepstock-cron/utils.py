# Importing Libraries
import os
import time
import json
import datetime
import pytz
from deta import Deta
from enum import Enum
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlencode

# configure your Deta project
deta = Deta("c0icbcyf_QaF3eiMteBeBrQTjPhu6GvPhoMGc13C6")
drive_mi = deta.Drive("market_info")  # access to your market_info drive
drive_si = deta.Drive("share_info")  # access to your share_info drive
db = deta.Base('market_info')


class Market(Enum):
    OPEN: str = "Market Open"
    CLOSED: str = "Market Close"


def crawler():
    """This function crawls nepstock website and returns some data.

    Returns:
        [type]: [description]
    """
    try:
        html = urlopen('http://www.nepalstock.com')
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('The server could not be found!')
    else:
        print('Website Successfully Crawled.')
    bs = BeautifulSoup(html.read(), 'html.parser')

    index = bs.find('div', {'class': {'current-index'}}).text.split()[0]
    market_status = bs.find(
        'div', {'id': 'top-notice-bar'}).find('b').text.strip()
    market_data = {data.text.split('|')[0]: data.text.split(
        '|')[1] for data in bs.find('div', {'id': 'market_info'}).find_all('span')}

    tables = bs.find('div', {'id': {'nepse-stats'}}).find_all('table',
                                                              {'class': {'table table-hover table-condensed'}})

    # get market summary
    market_summary = {}
    market_summary["title"] = tables[0].find("thead").find('td').text
    market_summary["data"] = {row.text.strip().split('\n')[0]: row.text.strip(
    ).split('\n')[1] for row in tables[0].find("tbody").findAll('tr')}
    # market_summary["data"]={}   #alternative method
    # for row in tables[0].find("tbody").findAll('tr'):
    #     k,v = row.text.strip().split('\n')
    #     market_summary["data"][k]=v

    market_information = {}
    for table in tables[1:]:
        for row in table.find("thead").findAll('tr'):
            t_head = [data.text for data in row.find_all(
                'td') if data.text != '']

        t_data = []
        for row in table.find("tbody").findAll('tr'):
            if len(row.text.strip()) > 0:
                t = {k: v.text.strip()
                     for k, v in zip(t_head, row.findAll('td'))}
                t_data.append(t)
        market_information[t_head[0]] = t_data
    return {
        "NEPSE_INDEX": index,
        "market_status": market_status,
        "market_data": market_data,
        "market_summary": market_summary,
        "market_information": market_information
    }


def share_price_crawler(upload: bool = False):
    """This function crawls nepstock website to get all the share prices.

    Returns:
        [type]: Share Data
    """
    try:
        data = urlencode({"_limit": "230"})
        data = data.encode('ascii')
        url = "http://www.nepalstock.com/todaysprice"
        html = urlopen(url, data)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('The server could not be found!')
    else:
        print('Website Successfully Crawled.')
    bs = BeautifulSoup(html.read(), 'html.parser')
    table = bs.find('table', {'class': {'table table-condensed table-hover'}})
    rows = [row for row in table.find_all(
        'tr') if len(row.find_all('td')) == 10]

    share_data = ''

    t_head = []
    for data in rows[0].find_all('td'):
        t_head.append(data.text)
    share_data = ','.join(t_head) + '\n'

    t_body = []
    for row in rows[1:]:
        r = {}
        for index, data in enumerate(row.find_all('td')):
            r[t_head[index]] = data.text.strip()
        share_data += ','.join(r.values()) + '\n'
        t_body.append(r)
    if upload:
        tz = pytz.timezone("Asia/Kathmandu")
        file_name = 'share_data_' + \
            datetime.datetime.now(tz).strftime("%Y_%m_%d-%I_%M_%S_%p")+'.csv'
        drive_si.put(file_name, share_data)
        print(f"File {file_name} uploaded to Deta successfully.")
    return t_head, t_body


def get_market_info(upload=False):
    crawler_data = crawler()
    market_open = crawler_data["market_status"] == Market.OPEN
    if upload and market_open:
        db.put({
            "index": crawler_data['NEPSE_INDEX'],
            "records": json.dumps(crawler_data),
            "created_at": time.ctime(time.time())
        })
        print("Data Written to database")
    return crawler_data


def get_share_info(upload=False):
    return share_price_crawler(upload)
