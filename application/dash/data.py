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
