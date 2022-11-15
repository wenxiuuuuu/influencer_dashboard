# Dash components, html, and dash tables
from dash import dcc 
from dash import html 
# Import Bootstrap components
import dash_bootstrap_components as dbc
from influencer_card import create_card


home_page = html.Div(
    className="row", 
    children=[
        html.Div("Hello website"),
        html.Div(id = "fb-root", children = []),
        
    ]
)

# influencer page 
row = [] 
for i in range(10): 
    row.append(create_card(i))

cards = dbc.Container(dbc.Row(row))

influencers_page = html.Div(
    cards
)

comparison_page = html.Div(
    children=[
        html.H1("Page 2")
    ]
)


