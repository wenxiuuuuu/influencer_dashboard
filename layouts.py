# Dash components, html, and dash tables
from dash import dcc 
from dash import html 
# Import Bootstrap components
import dash_bootstrap_components as dbc
from data import get_filtered_influ_df, rank_filtered_df
from influencer_card import create_card
from dash import Input, Output, State, callback
from data import dropdown_options 
from data import *
# from data import get_data_length
from mongodata import influencer_df
from mongodata import post_df
import pandas as pd

# def update_filtered_sorted_df(data= None):
#     print('updating filtered df')
#     filtered_sorted_df = data
#     return filtered_sorted_df

# filtered_sorted_df = pd.DataFrame()


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
                        value = 'fashion'
                        ),
                    ],
                    className="mb-3",
                    ), 
                html.Br(),
                html.Div([
                    dbc.Label("Follower Range", html_for="range-slider"), 
                    dcc.RangeSlider(id="follower_range", min=3000, max=50000, value=[10000,25000], allowCross=False, tooltip={'placement':'bottom', 'always_visible': False})
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
filtered_sorted_df = pd.DataFrame()
search_row = [] 

num_filtered_users = 10
results = pd.DataFrame()
sort_idx = []
@callback(
    output=Output(component_id="results", component_property="children"), 
    inputs=[Input(component_id="submit", component_property="n_clicks")], 
    state=[State("instagram", "value"), State("follower_range", "value"), State("category", "value")]
)
def save_info(n_clicks, instagram, follower_range, category): 

    # if n_clicks > 0: 
    #     ig_text = html.H4("instagram is: " + str(instagram))
    #     followers = html.H4("follower range is: " + str(follower_range[0]) + " to " + str(follower_range[1]))
    #     cate = html.H4("category is: " + str(category))
        
    #     # INFORMATION FROM COMPANY IS AVAILABLE HERE!! USE THIS PART TO TAKE DATA FOR FILTERS 

        # check if user exists in our companies db 
        # 1. filter the df
        filtered_df = get_filtered_influ_df(instagram, follower_range, category)
        # print(filtered_df)
        # 2. rank the users
        print("filtered")
        # 3. get the cards for each in their ranking order
        sorted_df = rank_filtered_df(filtered_df, category)
        sorted_indices = list(sorted_df.index)
        print("INDICES")
        print(sorted_indices)
        global filtered_sorted_df
        filtered_sorted_df = sorted_df
        global search_row
        for i in sorted_indices: 
            row.append(create_card(i, filtered_sorted_df))
        return success_msg, search_page

success_msg = html.Div(
    [
        html.Br(), 
        html.H4("Successful! Influencers you are matched with: ", style={"text-align": "center"})
    ])

# influencer page 
row = [] 
for i in influencer_df['username']: 
    row.append(create_card(i))

cards = dbc.Container(dbc.Row(row, style={"display": "flex", "align-items": "center", "justify-content": "center"}))
influencers_page = cards


comparison_page = html.Div(
    children=[
        html.H3("Compare Two Influencers", style={"margin-top": "30px", "text-align": "center"}), 
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id="dropdown_1",
                        options=dropdown_options(),
                        value=0,
                        style={"margin-left": "7px", "width": "97.8%"}
                        ),
                    html.Div(id="influencer-1"), 
                ]), 
                dbc.Col([
                    dcc.Dropdown(
                        id="dropdown_2",
                        options=dropdown_options(),
                        value=1, 
                        style={"margin-left": "7px", "width": "97.8%"}
                        ),
                    html.Div(id="influencer-2"), 
                ])
            ]), 
        ]), 
        html.Div(
            [dbc.Button("Submit", id="compare_options", n_clicks=0, style={"width": "20%"})], 
            style={"display": "flex", "align-items": "center", "justify-content": "center"}
        ),  
        html.Div(id='comparison')
    ]
)

@callback(
    output=Output(component_id="influencer-1", component_property="children"), 
    inputs=[Input(component_id="dropdown_1", component_property="value")]
)
def dropdown_one(dropdown_1): 
    influencer_one = dropdown_1
    return create_card(influencer_one, False)

@callback(
    output=Output(component_id="influencer-2", component_property="children"), 
    inputs=[Input(component_id="dropdown_2", component_property="value")]
)
def dropdown_two(dropdown_2): 
    influencer_two = dropdown_2
    return create_card(influencer_two, False)

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