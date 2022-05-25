"""Instantiate a Dash app."""
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash_table import DataTable, FormatTemplate
from .data import create_dataframe
from .layout import html_layout
import plotly.express as px
import math

millnames = ['',' K',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '${:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def create_data_table(df):
    """Create Dash datatable from Pandas Dataframe"""
    money = FormatTemplate.money(2)
    table = DataTable(
        id="database-table",
        columns=[{"name": i, "id":i, "format":money} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
        style_table={'overflowX': 'scroll', 'whiteSpace': 'normal','height': 'auto',},
    )
    return table

def create_card_new(card_data):
    def create_kfi(kfi, type):
        z = []
        if type == 'tab1':
            for x in kfi:
                kfi_f = html.Div([
                    html.H2(f"{kfi[x]['value']}"),
                    html.H5(f"{kfi[x]['name']}")])
                z.append(kfi_f)
                
        elif type == 'tab2':
            for x in kfi:
                z.append(html.H5(f"{kfi[x]['descr']}", style={'text-align':'left'}))
                
        elif type == 'tab3':
            for x in kfi:
                z.append(html.H5(f"{kfi[x]['name']} = {kfi[x]['calculation']}", style={'text-align':'left'}))
        
        zh = html.Div(children=z)
        return zh

    header = dbc.CardHeader( # Title and STatus
        [
            html.Div([html.H3(children=card_data['header']['title'])]),
            html.Div(children=html.Span(children=html.Span()),title='Online', className="dot green" if card_data['header']['status_dot'] == True else 'dot red')
        ], className='card-title-box'
    )

    tab1_content = dbc.CardBody([ # Summary
        create_kfi(card_data['kfi'], 'tab1'),
        html.Br(),
        html.H5(card_data['threshold'], style={'text-align':'left'}),
        html.Br(),]
    )

    tab2_content = dbc.CardBody([ # Definitions
        create_kfi(card_data['kfi'], 'tab2'),
        html.Br()]
    )

    tab3_content = dbc.CardBody([ # Calculations
        create_kfi(card_data['kfi'], 'tab3'),
        html.Br()]
    )

    tabs = dbc.Tabs( #footer thing
        [
            dbc.Tab(tab1_content, label="SUMMARY", tab_style={'border':'none'}),
            dbc.Tab(tab2_content, label="DEFINITIONS", tab_style={'border':'none'}),
            dbc.Tab(tab3_content, label="CALCULATIONS", tab_style={'border':'none'}),
        ], id='tabs2', style={'position':'absolute', 'bottom':'0', 'font-size':'1.5rem', 'border-bottom':'none'},persistence=True,
    )

    card = dbc.Card(
        [
            header,
            tabs
        ], style={'min-height':'300px'}
    )

    return card

def init_dashboard(server):
    """Created a Plotly Dash dashboard"""
    dash_app = Dash(
        name=__name__,
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/dist/css/s1.css",
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.come/css?family=Lato",
            dbc.themes.BOOTSTRAP
        ],
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1"}
        ]
    )

    # Load Dataframe
    df = create_dataframe() #Financial API Call

    # Custom HMTL layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(        
        children=[
            html.Div([
                html.Div([ # convert this to a form
                html.H3("Enter a company's stock ticker below:", style={'color':'white'}),
                html.Div([
                    html.Div(dcc.Input(id='input-on-submit', type='text', n_submit=0)),
                    html.Button('Submit', id='submit-val', n_clicks=0, className='button-1'),],
                    )
                ], 
                className="card_container one column")
            ], 
            className="row flex-display",),
            dbc.CardGroup([
                dcc.Graph(id='viz-1', style={'height': '45vh'}, className="card_container three columns card"),
                dcc.Graph(id='viz-2', style={'height': '45vh'}, className="card_container three columns card"),
                dcc.Graph(id='viz-3', style={'height': '45vh'}, className="card_container three columns card"),],
                ),
            dbc.CardGroup([
                dbc.Card(children=html.H3( id='card-1', children='Market Capitalization'), className="card_container three columns"),
                dbc.Card(children=html.H3( id='card-2', children='PE Ratio'), className="card_container three columns"),
                dbc.Card(children=html.H3( id='card-3', children='Current Ratio'), className="card_container three columns"),],
            ),
            dbc.CardGroup([
                dbc.Card(children=html.H3( id='card-4', children='Price vs Enterprise Value'), className="card_container three columns"),
                dbc.Card(children=html.H3( id='card-5', children='Required Growth'), className="card_container three columns"),
                dbc.Card(children=html.H3( id='card-6', children="Graham's Number"), className="card_container three columns"),], 
            ),
            html.Br(),
            create_data_table(df)
        ],
        id="dash-container",
    ) 
    @dash_app.callback(
        Output('viz-1', 'figure'),
        Output('viz-2', 'figure'),
        Output('viz-3', 'figure'),
        Output('card-1', 'children'),
        Output('card-2', 'children'),
        Output('card-3', 'children'),
        Output('card-4', 'children'),
        Output('card-5', 'children'),
        Output('card-6', 'children'),
        Output("database-table", 'data'),
        Output("database-table", 'columns'),
        Input('input-on-submit', "n_submit"),
        Input('submit-val', "n_clicks"),
        State('input-on-submit', 'value'))

    def update_table(n_submit, n_clicks, value):
        if value is None:
            return 
        value = value.rstrip()
        ticker = str(value.upper())
        dfs = create_dataframe(ticker)

        # ================================================
        # Viz 1 - line graph
        # ================================================
        viz1 = px.line(dfs, 
                x="date", 
                y="revenue", 
                title=f"Quarterly Revenue for {ticker}" if ticker is not None else f"revenuePerShare",
                hover_name="symbol",
                markers=True
        )
        viz1.add_hline(y=700000000) #$700M min required
        viz1.update_layout(
            transition_duration=500
        )

        # ================================================
        # Viz 2 - line graph
        # ================================================
        viz2 = px.line(dfs, 
                x="date", 
                y="netIncome", 
                title=f"Quarterly Net Income for {ticker}" if ticker is not None else f"netIncome",
                hover_name="symbol",
                markers=True
        )
        # viz2.add_hline(y=700000000) 
        viz2.update_layout(
            transition_duration=500
        )
        
        # ================================================
        # Viz 3 - line graph
        # ================================================
        viz3 = px.line(dfs, 
                x="date", 
                y="stockPrice", 
                title=f"Quarterly Stock Price for {ticker}" if ticker is not None else f"stockPrice",
                hover_name="symbol",
                markers=True
        )
        viz3.update_layout(
            transition_duration=500
        )

        # ================================================
        # Card 1
        # ================================================
        formattedMarketCap = millify(dfs.marketCap[dfs.marketCap.first_valid_index()])
        formattedCurrentAssetValueMult = millify(dfs.totalCurrentAssets[dfs.totalCurrentAssets.first_valid_index()]*1.5)
        marketCapCurrentAssetPass = True if dfs.marketCap[dfs.marketCap.first_valid_index()] <= dfs.totalCurrentAssets[dfs.totalCurrentAssets.first_valid_index()]*1.5 else False

        card_data = {
            "header": { "title": "Market Capitalization", "status_dot": marketCapCurrentAssetPass},
            "kfi": {
                1 : {
                    "value": formattedMarketCap,
                    "name": "Market Capitalization",
                    "descr" : "Market Capitalization is the total value of all a company's shares of stock.",
                    "calculation": "Stock Price x Shares Outstanding"}, 
                2 : {
                    "value": formattedCurrentAssetValueMult,
                    "name": "Current Asset Value 1.5",
                    "descr" : "Current Asset Value is the total value of all of a company's current assets x 1.5.",
                    "calculation": "Current Assets - (Total Liabilities + Preferred Stock)"}, 
                },
            "threshold":f"Market Capitalization should be less than or equal to {formattedCurrentAssetValueMult}"}
        card1 = create_card_new(card_data)
        
        # Card 2
        # ================================================
        formattedPriceEarningsRatio = "{:,.2f}".format(dfs.peRatio[dfs.peRatio.first_valid_index()])
        priceEarningsRatioPass = True if dfs.peRatio[dfs.peRatio.first_valid_index()] <= 15 else False

        card_data2 = {
            "header": { "title": "Price Equity Ratio", "status_dot": priceEarningsRatioPass},
            "kfi": {
                1 : {
                    "value": formattedPriceEarningsRatio,
                    "name": "Price-Earnings Ratio",
                    "descr" : "Price-Earnings Ratio values a company by comparing its share price to its earnings per share .",
                    "calculation": "Price per share / Earnings per Share "}
                },
            "threshold":f"Price-Earnings Ratio should be less than or equal to 15. This means the current market value of the company is equal to 15x its annual earnings."}
        card2 = create_card_new(card_data2)

        # Card 3
        # ================================================
        formattedCurrentRatio = "{:,.2f}".format(dfs.currentRatio[dfs.currentRatio.first_valid_index()])
        currentRatioPass = True if dfs.currentRatio[dfs.currentRatio.first_valid_index()] >= 2 else False

        card_data3 = {
            "header": { "title": "Current Ratio", "status_dot": currentRatioPass},
            "kfi": {
                1 : {
                    "value": formattedCurrentRatio,
                    "name": "Current Ratio",
                    "descr" : "Current Ratio measures a company's ability to pay short-term obligations or those due within one year. It tells investors and analysts how a company can maximize the current assets on its balance sheet to satisfy its current debt and other payables.",
                    "calculation": "Current Assets / Current Liabilities "}
                },
            "threshold":f"Current Ratio should be between 1.5 and 2.5. A ratio less than 1 may indicate debts due in a year or less are greater than its assets. A high ratio (>3) may indicate that a company is not using its current assets efficiently, securing financing very well, or properly managing its working capital."}
        card3 = create_card_new(card_data3)


        # ================================================

        # Card 4
        # ================================================
        price = dfs.stockPrice[dfs.stockPrice.first_valid_index()] * dfs.sharesOutstanding[dfs.sharesOutstanding.first_valid_index()]
        enterpriseValue = dfs.enterpriseValue[dfs.enterpriseValue.first_valid_index()]*0.667 / dfs.sharesOutstanding[dfs.sharesOutstanding.first_valid_index()]
        formattedEnterpriseValue = "${:,.2f}".format(enterpriseValue)
        formattedPrice = "${:,.2f}".format(dfs.stockPrice[dfs.stockPrice.first_valid_index()])
        marginOfSafetyPass = True if price <= enterpriseValue else False

        card_data4 = {
            "header": { "title": "Price vs Enterprise Value", "status_dot": marginOfSafetyPass},
            "kfi": {
                1 : {
                    "value": formattedPrice,
                    "name": "Price",
                    "descr" : "Price refers to the stock price of the company as reported at the most recent quarterly earnings report.",
                    "calculation": "Stock price"},
                2 : {
                    "value": formattedEnterpriseValue,
                    "name": "Adjusted Enterprise Value",
                    "descr" : "Enterprise Value is a measure of a company's total value, often used as a more comprehensive alternative to equity market capitalization. Enterprise Value is a popular metric used to value a company for a potential takeover. Adjusted Enterprise Value = Enterprise Value x 66.67%",
                    "calculation": "Enterprise Value = Market Capitalization + Total Debt - Cash and Cash Equivalents"}
                },
            "threshold":f"Price should be less than or equal to Adjusted Enterprise Value."}
        card4 = create_card_new(card_data4)

        # Card 5
        # ================================================
        enterpriseValueFull = dfs.enterpriseValue[dfs.enterpriseValue.first_valid_index()]
        earnings = dfs.netIncome[dfs.netIncome.first_valid_index()]
        requiredGrowth = 2*((enterpriseValueFull/earnings)-8.5)
        formattedRequiredGrowth = "{:,.2f}%".format(requiredGrowth)

        card_data5 = {
            "header": { "title": "Required Growth", "status_dot":""},
            "kfi": {
                1 : {
                    "value": formattedRequiredGrowth,
                    "name": "Required Growth",
                    "descr" : "Required Growth shows the growth in revenue required over a 7-10 year period to justify purchasing at today's stock price.",
                    "calculation": "2 x (Enterprise Value / Net Income) - 8.5"}
                },
            "threshold":f"Shows the earnings growth required over a 7-10 year period to rationalize today's stock price."}
        card5 = create_card_new(card_data5)

        # Card 6
        # ================================================
        grahamNumber = dfs.grahamNumber[dfs.grahamNumber.first_valid_index()]
        formattedGrahamNumber = "{:,.2f}".format(grahamNumber)
        grahamNumberPass = True if dfs.stockPrice[dfs.stockPrice.first_valid_index()] <= grahamNumber else False 
        
        card_data6 = {
            "header": { "title": "Graham's Number vs Stock Price", "status_dot": grahamNumberPass},
            "kfi": {
                1 : {
                    "value": formattedGrahamNumber,
                    "name": "Graham's Number",
                    "descr" : "Graham's Number measures a stock's fundamental value by taking into account the company's earnings per share (EPS) and book value per share (BVPS). The Graham number is the upper bound of the price range that a defensive investor should pay for the stock. According to the theory, any stock price below the Graham number is considered undervalued and thus worth investing in. The 22.5 in the calculation comes from a limit on the P/E Ratio being no more than 15, and the Book-value per Share being no more than 1.5, thus 15x1.5=22.5",
                    "calculation": "(22.5 x (Net Income / Shares Outstanding) x (Shareholder's Equity / Shares Outstanding))^1/2"},
                2 : {
                    "value": formattedPrice,
                    "name": "Stock price",
                    "descr" : "Price refers to the stock price of the company as reported at the most recent quarterly earnings report.",
                    "calculation": "Stock price"}
                },
            "threshold":f"Don't pay more than Graham's Number."}
        card6 = create_card_new(card_data6)

        columns=[{"name": i, "id":i} for i in dfs.columns]
        data=dfs.to_dict("records")

        return viz1, viz2, viz3, card1, card2, card3, card4, card5, card6, data, columns
            
    return dash_app.server