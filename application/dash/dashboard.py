"""Instantiate a Dash app."""
from dash import Dash, dcc, html, Input, Output, State
from dash_table import DataTable, FormatTemplate
from .data import create_dataframe
from .layout import html_layout
import plotly.express as px

def init_dashboard(server):
    """Created a Plotly Dash dashboard"""
    dash_app = Dash(
        name=__name__,
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/dist/css/s1.css",
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.come/css?family=Lato"
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
                html.H3("Enter a company's stock ticker below:"),
                html.Div([
                    html.Div(dcc.Input(id='input-on-submit', type='text', n_submit=0)),
                    html.Button('Submit', id='submit-val', n_clicks=0, className='button-1'),],
                    )
                ], 
                className="card_container one column")
            ], 
            className="row flex-display",),
            html.Div([
                dcc.Graph(id='viz-1', style={'height': '45vh'}, className="card_container three columns"),
                dcc.Graph(id='viz-2', style={'height': '45vh'}, className="card_container three columns"),
                dcc.Graph(id='viz-3', style={'height': '45vh'}, className="card_container three columns"),],
                className="row flex-display",),
            html.Div([
                html.Div(children=[html.H5(id='card-1', children='Market Capitalization')], className="card_container three columns"),
                html.Div(children=html.H5(id='card-2', children='PE Ratio'), className="card_container three columns"),
                html.Div(children=html.H5( id='card-3', children='Current Ratio'), className="card_container three columns"),], 
                className="row flex-display",),
            html.Div([
                html.Div(children=html.H5( id='card-4', children='Price vs Enterprise Value'), className="card_container three columns"),
                html.Div(children=html.H5( id='card-5', children='Required Growth'), className="card_container three columns"),
                html.Div(children=html.H5( id='card-6', children="Graham's Number"), className="card_container three columns"),], 
                className="row flex-display",),
            html.Br(),
            # 1. Add a figX here 
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
        formattedMarketCap = "${:,.2f}".format(dfs.marketCap[dfs.marketCap.first_valid_index()])
        formattedCurrentAssetValue = "${:,.2f}".format(dfs.totalCurrentAssets[dfs.totalCurrentAssets.first_valid_index()])
        formattedCurrentAssetValueMult = "${:,.2f}".format(dfs.totalCurrentAssets[dfs.totalCurrentAssets.first_valid_index()]*1.5)
        marketCapCurrentAssetPass = True if dfs.marketCap[dfs.marketCap.first_valid_index()] >= dfs.totalCurrentAssets[dfs.totalCurrentAssets.first_valid_index()]*1.5 else False
        formattedDiff = "${:,.2f}".format(dfs.totalCurrentAssets[dfs.totalCurrentAssets.first_valid_index()]*1.5)
        card1 = html.Div([
            html.Div([
                html.Div([html.H5(children='Market Capitalization')]),
                html.Div(children=html.Span(children=html.Span()),title='Online', 
                    className="dot green" if marketCapCurrentAssetPass == True else 'dot red'),
            ],className='card-title-box'),
            html.Div([
                html.H2(f"{formattedMarketCap}"),
                html.H5('Market Cap should be less than or equal to  ' + f"{formattedCurrentAssetValueMult}*"), 
                html.H6(children=['*Net Current Asset Value x 1.5', html.Br(), f"i.e.: {formattedCurrentAssetValue} x 1.5 = {formattedCurrentAssetValueMult}"], className='note')
            ],className='card-content-box'),],
            id='card-1',
        )
        
        # Card 2
        # ================================================
        formattedPriceEarningsRatio = "{:,.2f}".format(dfs.peRatio[dfs.peRatio.first_valid_index()])
        priceEarningsRatioPass = True if dfs.peRatio[dfs.peRatio.first_valid_index()] <= 15 else False
        card2 = html.Div([
            html.Div([
                html.Div([html.H5(children='Price Equity Ratio')]),
                html.Div(children=html.Span(children=html.Span()),title='Online', 
                    className="dot green" if priceEarningsRatioPass == True else 'dot red'),
            ],className='card-title-box'),
            html.Div([
                html.H2(f"{formattedPriceEarningsRatio}"),
                html.H5('Price-Equity Ratio should be less than or equal to 15')
            ],className='card-content-box'),],
            id='card-2',
        )
        # ================================================

        # Card 3
        # ================================================
        formattedCurrentRatio = "{:,.2f}".format(dfs.currentRatio[dfs.currentRatio.first_valid_index()])
        currentRatioPass = True if dfs.currentRatio[dfs.currentRatio.first_valid_index()] >= 2 else False
        card3 = html.Div([
            html.Div([
                html.Div([html.H5(children='Current Ratio')]),
                html.Div(children=html.Span(children=html.Span()),title='Online', 
                    className="dot green" if currentRatioPass == True else 'dot red'),
            ],className='card-title-box'),
            html.Div([
                html.H2(f"{formattedCurrentRatio}"),
                html.H5('Current Ratio should be greater than or equal to 2')
            ],className='card-content-box'),],
            id='card-3',
        )
        # ================================================

        # Card 4
        # ================================================
        price = dfs.stockPrice[dfs.stockPrice.first_valid_index()] * dfs.sharesOutstanding[dfs.sharesOutstanding.first_valid_index()]
        enterpriseValue = dfs.enterpriseValue[dfs.enterpriseValue.first_valid_index()]*0.667 / dfs.sharesOutstanding[dfs.sharesOutstanding.first_valid_index()]
        formattedEnterpriseValue = "${:,.2f}".format(enterpriseValue)
        formattedPrice = "${:,.2f}".format(dfs.stockPrice[dfs.stockPrice.first_valid_index()])
        marginOfSafetyPass = True if price <= enterpriseValue else False
        card4 = html.Div([
            html.Div([
                html.Div([html.H5(children='Price vs Enterprise Value')]),
                html.Div(children=html.Span(children=html.Span()),title='Online', 
                    className="dot green" if marginOfSafetyPass == True else 'dot red'),
            ],className='card-title-box'),
            html.Div([
                html.H2(f"Price: {formattedPrice}"),
                html.H2(f"Adjusted Enterprise Value: {formattedEnterpriseValue} (target)"),
                html.H5('Price should be less than or equal to Adjusted Enterprise Value*'),
                html.H6(children=["*i.e.: Price <= Adjusted Enterprise Value;", html.Br(), "Price = Stock Price x Shares Outstanding;", html.Br(),"Adjusted Enterprise Value = 2/3 * Enterprise Value / Shares Outstanding;",],
                    className='note')
            ],className='card-content-box'),
            ],
            id='card-4',
        )
        # ================================================

        # Card 5
        # ================================================
        enterpriseValueFull = dfs.enterpriseValue[dfs.enterpriseValue.first_valid_index()]
        earnings = dfs.netIncome[dfs.netIncome.first_valid_index()]
        requiredGrowth = 2*((enterpriseValueFull/earnings)-8.5)

        formattedRequiredGrowth = "{:,.2f}%".format(requiredGrowth)
        card5 = html.Div([
            html.Div([
                html.Div([html.H5(children='Required Growth')]),
                html.Div(children=html.Span(children=html.Span()),title='Online', 
                    className="dot yellow"),
            ],className='card-title-box'),
            html.Div([
                html.H2(f"{formattedRequiredGrowth} per year"),
                html.H5("Shows the earnings growth required over a 7-10 year period to rationalize today's stock price"),
                html.H6("Does this growth seem reasonable?", 
                    className='note')
            ],className='card-content-box')],
            id='card-5',
        )
        # ================================================

        # Card 6
        # ================================================
        grahamNumber = dfs.grahamNumber[dfs.grahamNumber.first_valid_index()]
        formattedGrahamNumber = "{:,.2f}".format(grahamNumber)
        grahamNumberPass = True if dfs.stockPrice[dfs.stockPrice.first_valid_index()] <= grahamNumber else False 
        card6 = html.Div([
            html.Div([
            html.Div([html.H5(children="Graham's Number vs Stock Price")]),
                html.Div(children=html.Span(children=html.Span()),title='Online', 
                    className="dot green" if grahamNumberPass == True else 'dot red'),
            ],className='card-title-box'),
            html.Div([
                html.H2(f"Graham's Number: {formattedGrahamNumber}"),
                html.H5(f"Stock price: {formattedPrice}"),
                html.H6("Don't pay more than Graham's Number", 
                    className='note')
            ],className='card-content-box')],
            id='card-6',
        )
        # ================================================

        columns=[{"name": i, "id":i} for i in dfs.columns]
        data=dfs.to_dict("records")


        return viz1, viz2, viz3, card1, card2, card3, card4, card5, card6, data, columns
            
    return dash_app.server


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
