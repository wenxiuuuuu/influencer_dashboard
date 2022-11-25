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

from layouts import (home_page, sort_layout, comparison_page, influencer_network_page, cluster_page)
# from data import get_card_data

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-db", "--dbtype", help="MONGO / CSV")
args = parser.parse_args()
database_type = args.dbtype

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.LUX, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'],
    suppress_callback_exceptions=True
)
server = app.server

app.title = "Influ-Finder"

# app = Dash(name, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="home")),
        dbc.NavItem(dbc.NavLink("Comparison", href="comparison")),
        # dbc.NavItem(dbc.NavLink("Influencers", href="influencers")),
        dbc.DropdownMenu(
            children=[
                # dbc.DropdownMenuItem("Influencers", header=True),
                dbc.DropdownMenuItem("Show All", href="influencer_show"),
                dbc.DropdownMenuItem("Network", href="influencer_network"),
                dbc.DropdownMenuItem("Image Cluster", href="influencer_cluster"),
            ],
            nav=True,
            in_navbar=True,
            label="Influencers",
        )
        ],
    brand="Influ-Finder",
    brand_href="/home",
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
    if pathname == '/influencer_show':
        return navbar, sort_layout
        # return navbar, filter_layout
    elif pathname == '/comparison':
        return navbar, comparison_page
    elif pathname == '/home':
        return navbar, home_page
    elif pathname == '/influencer_network':
        return navbar, influencer_network_page
    elif pathname == '/influencer_cluster':
        return navbar, cluster_page

if __name__ == '__main__':
    app.run_server(debug=True)
