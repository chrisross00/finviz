from dotenv import load_dotenv
import numpy as np
import pandas as pd
import os
import fmpsdk
from dotenv import load_dotenv

"""This is where we put the API and data-handling stuff"""
load_dotenv()
apikey = os.environ.get("FMP_API_KEY")

def create_dataframe_old(ticker='AAPL'):
    """Create Pandas Dataframe from fmpsdk API."""
    # ticker = str(ticker.upper())
    symbol: str = str(ticker)
    CompanyProfile = fmpsdk.income_statement(apikey=apikey, symbol=symbol)
    df = pd.DataFrame(CompanyProfile)
    df.replace(np.nan)
    return df

def create_dataframe(ticker=''):
    symbol: str = str(ticker)
    # ticker = str(ticker.upper())
    
    # Uncomment for API
    incomeStatement = fmpsdk.income_statement(apikey=apikey, symbol=symbol, period='quarter')
    balanceSheet = fmpsdk.balance_sheet_statement(apikey=apikey, symbol=symbol, period='quarter')
    keyMetrics = fmpsdk.key_metrics(apikey=apikey, symbol=symbol, period='quarter')
    quote = fmpsdk.quote(apikey=apikey, symbol=symbol)
    enterpriseValues = fmpsdk.enterprise_values(apikey=apikey, symbol=symbol, period='quarter')

    list = (
        incomeStatement,
        balanceSheet,
        keyMetrics,
        quote,
        enterpriseValues)
    preDf = []
    for i in list:
        for j in i:
            preDf.append(j)

    # # preDf = pd.read_csv('data/df') # Comment this for offline mode OFF
    # # preDF = pd.read_csv('data/AAPL') if ticker == 'AAPL' else pd.read_csv('data/TSLA')
    df = pd.DataFrame(preDf)
    df.fillna('')
    return df

"""different dataframes I need

Note: df = create_dataframe()

- fmpsdk.income_statement
    - Annual Revenue = df.revenue
    - earnings per share = df.eps
    - gross_profit
    - netIncome

- fmpsdk.balance_sheet_statement
    - d.totalAssets
    - d.totalCurrentAssets
    - d.totalLiabilities
    - d.totalCurrentLiabilities

- fmpsdk.key_metrics_ttm
    - netCurrentAssetValueTTM
    - workingCapitalTTM 
    - bookValuePerShareTTM
    - grahamNumberTTM
    - Current Ratio = df.currentRatio
    - PE Ratio = df.priceEarningsRatio -  The price/earnings ratio conveys how much investors will pay per share for $1 of earnings.
    - d.bookValuePerShareTTM
    - marketCapTTM 

- fmpsdk.quote
    - price
    - sharesOutstanding
    - marketCap

- fmpsdk.enterprise_values
    - enterpriseValue

"""



""" 
Sorting into different visualization types

Cards/Numbers:
- marketCapTTM >= $700m
- enterpriseValue




- Annual Revenue = df.revenue > $700 million
- Current Ratio = df.currentRatio  >= 200%
- marketCapTTM <= 1.5*netCurrentAssetValueTTM
    - going to go with totalCurrentAssets because netCurrentAsset is weird
- PE Ratio = df.priceEarningsRatio < 15


- price <= .667*enterpriseValue
- price <= workingCapitalTTM
- required growth = 2 * ( ( enterpriseValue / earnings ) - 8.5 )



- earnings per share = df.eps
    - net income - preferredDividends / sharesOutstanding
- d.totalAssets
- d.totalCurrentAssets
- d.totalLiabilities
- d.totalCurrentLiabilities


- bookValuePerShareTTM
- grahamNumberTTM
- d.bookValuePerShare or d.bookValuePerShareTTM

value as enterpriseValue
OR
value as 

earnings as earningsPerShare x sharesOutstanding
OR
earnings as grossProfit = 152,836,000,000   152836000000/16701272000
OR 
earnings as Assets - Liabilities = 351002000000 - 287912000000 = 63,090,000,000

"""

grossProfit = 152836000000

so = 16185199991

eps = 5.67






# CompanyProfile = pd.read_csv('data/AAPL') if ticker == 'AAPL' else pd.read_csv('data/TSLA') 


"""Things that should maybe be calculated instead of pulled:
- Graham's number
- bookValuePerShare
- earningsPerShare
- 

"""
