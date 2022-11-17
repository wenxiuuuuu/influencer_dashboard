# Dash components, html, and dash tables
from dash import dcc 
from dash import html 
# Import Bootstrap components
import dash_bootstrap_components as dbc
from influencer_card import create_card
from dash import Input, Output, State, callback
from data import dropdown_options 


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
        return success_msg, influencers_page

success_msg = html.Div(
    [
        html.Br(), 
        html.H4("Successful! Influencers you are matched with: ", style={"text-align": "center"})
    ])

# influencer page 
row = [] 
for i in range(10): 
    row.append(create_card(i))

cards = dbc.Container(dbc.Row(row))

influencers_page = cards

comparison_page = html.Div(
    className="container", 
    children=[
        html.H3("Compare Two Influencers", style={"margin-top": "30px", "text-align": "center"}), 
        html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id="dropdown_1",
                        options=dropdown_options(),
                        value=1
                        ),
                    html.Div(id="influencer-1"), 
                    
                ]), 
                dbc.Col([
                    dcc.Dropdown(
                        id="dropdown_2",
                        options=dropdown_options(),
                        value=2
                        ),
                    html.Div(id="influencer-2"), 
                ])
            ]), 
        ]), 
        dbc.Button("Submit", id="compare_options", n_clicks=0, style={"width": "30%", "justify-content": "center", "display": "flex"}), 
        html.Div(id='comparison')
    ]
)

@callback(
    output=Output(component_id="influencer-1", component_property="children"), 
    inputs=[Input(component_id="dropdown_1", component_property="value")]
)
def dropdown_one(dropdown_1): 
    influencer_one = dropdown_1
    return create_card(influencer_one)

@callback(
    output=Output(component_id="influencer-2", component_property="children"), 
    inputs=[Input(component_id="dropdown_2", component_property="value")]
)
def dropdown_two(dropdown_2): 
    influencer_two = dropdown_2
    return create_card(influencer_two)

@callback(
    output=Output(component_id="comparison", component_property="children"), 
    inputs=[Input(component_id="compare_options", component_property="n_clicks"), 
    Input(component_id='dropdown_1', component_property="value"), Input(component_id='dropdown_2', component_property="value")]
)
def show_comparison(compare_options, dropdown_1, dropdown_2): 
    if compare_options>0: 
        result = html.H3("choice 1 is " + str(dropdown_1) + " choice2 is " + str(dropdown_2))
    # result = html.H3("Please make your choice!")
        return result