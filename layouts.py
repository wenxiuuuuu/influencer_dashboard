# Dash components, html, and dash tables
from dash import dcc 
from dash import html 
# Import Bootstrap components
import dash_bootstrap_components as dbc
from influencer_card import create_card
from dash import Input, Output, State, callback 


# home page!
home_page = html.Div(
    [   
        html.Div(
            className="container",
            children=[
                html.H3("Welcome! Please input your company details for us to find your influencer matches :)", 
                    style={"margin-top": "30px", "text-align": "center"}),
                html.Br(),
                html.Div([
                    dbc.Label("Company instagram", html_for="example-ig"), 
                    dbc.Input(id="instagram", placeholder="Eg @netflixsg"), 
                ]),
                html.Br(),
                html.Div([
                    dbc.Label("Company Category", html_for="dropdown"),
                    dcc.Dropdown(
                        id="category",
                        options=[
                            {"label": "Fashion", "value": "fashion"},
                            {"label": "Fitness", "value": "fitness"},
                            {"label": "Lifestyle", "value": "lifestyle"},
                            {"label": "Food", "value": "food"},
                            ],
                        ),
                    ],
                    className="mb-3",
                    ), 
                html.Br(),
                html.Div([
                    dbc.Label("Follower Range", html_for="range-slider"), 
                    dcc.RangeSlider(id="follower_range", min=3000, max=50000, 
                                value=[10000,25000])
                ], 
                className="mb-3"), 
                html.Br(), 
                dbc.Button('Submit', id='submit', n_clicks=0, style={"width": "30%", "margin": "auto"}),
            ],
            style={"width": "40%", "display": "grid"}
        ), 
        html.Div(
            id="results"
        )
        ]
        
    
)

@callback(
    output=Output(component_id="results", component_property="children"), 
    inputs=[Input(component_id="submit", component_property="n_clicks")], 
    state=[State("instagram", "value"), State("follower_range", "value"), State("category", "value")]
)
def save_info(n_clicks, instagram, follower_range, category): 
    if n_clicks > 0: 
        ig_text = html.H4("instagram is: " + str(instagram))
        followers = html.H4("follower range is: " + str(follower_range[0]) + " to " + str(follower_range[1]))
        cate = html.H4("category is: " + str(category))
        
        # INFORMATION FROM COMPANY IS AVAILABLE HERE!! USE THIS PART TO TAKE DATA FOR FILTERS 

        # return ig_text, followers, cate
        return influencers_page


# influencer page 
row = [] 
for i in range(5): 
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


