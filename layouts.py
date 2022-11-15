# Dash components, html, and dash tables
from dash import dcc 
from dash import html 
# Import Bootstrap components
import dash_bootstrap_components as dbc
from influencer_card import create_card

# home page!
home_page = html.Div(
    className="container", 
    children=[
        html.H3("Welcome! Please input your company details for us to find your influencer matches :)", 
            style={"margin-top": "30px", "text-align": "center"}),
        html.Br(),
        html.Div([
            dbc.Label("Company instagram", html_for="example-ig"), 
            dbc.Input(type="instagram", id="company-ig", placeholder="Eg @netflixsg"), 
        ]),
        html.Br(),
        html.Div([
            dbc.Label("Company Category", html_for="dropdown"),
            dcc.Dropdown(
                id="category",
                options=[
                    {"label": "Fashion", "value": 1},
                    {"label": "Fitness", "value": 2},
                    {"label": "Lifestyle", "value": 3},
                    {"label": "Food", "value": 4},
                    ],
                ),
            ],
            className="mb-3",
            ), 
        html.Br(),
        html.Div([
            dbc.Label("Follower Range", html_for="range-slider"), 
            dcc.RangeSlider(id="follower-range", min=3000, max=50000, 
                        value=[10000,25000])
        ], 
        className="mb-3"), 
        html.Br(), 
        dbc.Button('Submit', id='submit', n_clicks=0, style={"width": "30%", "margin": "auto"}),
        
    ],
    style={"width": "40%", "display": "grid"}
)

# influencer page 
row = [] 
for i in range(23): 
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


