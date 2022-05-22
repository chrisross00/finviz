# Roadmap

## Priority
* Set up a new app using the factory pattern so it doesn't suck ass when you're further along

## Notes
* *Actviate Virtual Environtment*
  * cli: C**:\Users\chris\Documents\Projects\investviz> `finviz\Scripts\activate`

* Plotly Flask guide
  * https://hackersandslackers.com/plotly-dash-with-flask/
  
* Flask App Factory pattern
  * https://hackersandslackers.com/flask-application-factory/

* Financial Modeling Prep API
  * https://site.financialmodelingprep.com/developer/docs/dashboard

* Once you have a DF
  * >>> df.to_csv('./nameoffile') 

## Backlog
* Change the exchange type
* search for multiple quotes
* save searches / dashboard for saved searches
* login/logout/user profiles
* UI Stuff
  * Dash bootstrap components
  * Tooltips 
  * Live quotes etc
    * idea of context: a sticky or persistent set of divs could be interesting to play with
* News
  * Is there an easy way to pull news back?

## Done!




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

## **Notes on metrics and data:**
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



Things that should maybe be calculated instead of pulled:
- Graham's number
- bookValuePerShare
- earningsPerShare
- 
