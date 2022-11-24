import httpx
import pandas as pd
import datetime as dt
import streamlit as st
import sqlite3
import json
import time
import darts


def getMarketPrices(inplace=False):
    print('Fetching market prices')
    r = httpx.get(
        'https://esi.evetech.net/latest/markets/prices/?datasource=tranquility',)
    if (r.status_code == 200):
        df = pd.read_json(r.text)
        df['date'] = dt.datetime.now()
        con = sqlite3.connect('../data/data.db')
        df.to_sql(con=con, name="market_data", if_exists="append")
        con.close()
        if (inplace):
            return (df)
        # cur = con.cursor()
        # cur.execute('select * from market_data')
        # results = cur.fetchall()
        # print(results)
    else:
        print(f"Request did not succeed! {r.status_code}")
        rjson = json.loads(r.text)
        if (rjson['timeout'] != None or 0):
            time.sleep((rjson['timeout']/1000))


def dataCronJob():
    while (True):
        time.sleep(60)
        getMarketPrices()

if __name__ == '__main__':
    dataCronJob()
