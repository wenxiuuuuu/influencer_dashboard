import json
import base64
import datetime
import requests
import pathlib
import math
import pandas as pd
import flask
import dash
from dash import Dash, callback
from dash import dcc
from dash import html
from chart_studio import plotly as py
import plotly.graph_objs as go

from plotly import subplots
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container

from layouts import (home_page, influencers_page, comparison_page)
# from data import get_card_data

import argparse 
parser = argparse.ArgumentParser()

parser.add_argument("-db", "--dbtype", help="MONGO / CSV")
args = parser.parse_args()
database_type = args.dbtype

app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True
)

app.title = "Influ-Finder"

# app = Dash(name, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="home")),
        dbc.NavItem(dbc.NavLink("Influencers", href="influencers")),
        dbc.NavItem(dbc.NavLink("Comparison", href="comparison"))
        ],
    brand="Influ-Finder",
    brand_href="/",
    sticky='top'
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update the index
@callback(Output('page-content', 'children'),
         [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/influencers':
        return navbar, influencers_page
        # return navbar, filter_layout
    elif pathname == '/comparison':
        return navbar, comparison_page
    else:
        return navbar, home_page

if __name__ == '__main__':
    app.run_server(debug=True)
