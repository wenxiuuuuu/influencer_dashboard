# Dash components, html, and dash tables
from dash import html, dcc, Input, Output, State, callback
# Import Bootstrap components
import dash_bootstrap_components as dbc
# from data import get_filtered_influ_df, rank_filtered_df
from influencer_card import create_card, create_stats_table
# from data import dropdown_options 
from data import *
from mongodata import influencer_df, post_df
import pandas as pd
import dash_echarts
from echarts import option_graph, create_bar

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
                html.H3("Welcome! Please input your company details below:", 
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
                            {"label": "Health", "value": "health"},
                            # {"label": "Clothing (Brand)", "value": "Clothing (Brand)"},
                            # {"label": "Actor", "value": "Actor"},
                            # {"label": "Jewelry/watches", "value": "Jewelry/watches"},
                            # {"label": "Food & beverage", "value": "Food & beverage"},
                            ],
                        value = 'fashion'
                        ),
                    ],
                    className="mb-3",
                    ), 
                html.Br(),
                html.Div([
                    dbc.Label("Preferred Follower Range for Influencer", html_for="range-slider"), 
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
    inputs=[Input(component_id="submit", component_property="n_clicks"), Input("instagram", "value"), Input("follower_range", "value"), Input("category", "value")], 
    # state=[State("instagram", "value"), State("follower_range", "value"), State("category", "value")]
)
def save_info(n_clicks, instagram, follower_range, category): 
    print(n_clicks, instagram, follower_range, category)

    if n_clicks > 0: 
    #     ig_text = html.H4("instagram is: " + str(instagram))
    #     followers = html.H4("follower range is: " + str(follower_range[0]) + " to " + str(follower_range[1]))
    #     cate = html.H4("category is: " + str(category))
        
    #     # INFORMATION FROM COMPANY IS AVAILABLE HERE!! USE THIS PART TO TAKE DATA FOR FILTERS 

    # check if user exists in our companies db 
    # 1. filter the df
        filtered_df = get_filtered_influ_df(instagram, follower_range, category)
        # print('filtered_df', filtered_df)
        # 2. rank the users
        print("filtered")
        # 3. get the cards for each in their ranking order
        sorted_df = rank_filtered_df(filtered_df, category)
        sorted_usernames = list(sorted_df['username'])
        print("INDICES")
        print(sorted_usernames)
        global filtered_sorted_df
        filtered_sorted_df = sorted_df
        global search_row
        search_row = [] 
        for i in sorted_usernames: 
            search_row.append(create_card(i))
        search_cards = dbc.Container(dbc.Row(search_row, style={"display": "flex", "align-items": "center", "justify-content": "center"}))
        search_page = search_cards
        if sorted_usernames:
            success_msg = html.Div(
            [
                html.Br(), 
                html.H4(f"Successful! You are matched with {len(sorted_usernames)} influencers!", style={"text-align": "center"})
            ])
        else: 
            success_msg = html.Div(
            [
                html.Br(), 
                html.H4("Sorry... No influencers is matched with your company...", style={"text-align": "center"}),
                html.H6("Try adjusting your preferred follower range.", style={"text-align": "center"})
            ])

        return success_msg, search_page
    return html.Div()


# influencer page 
row = [] 
for i in influencer_df['username']: 
    row.append(create_card(i))

cards = dbc.Container(dbc.Row(row, style={"display": "flex", "align-items": "center", "justify-content": "center"}))
influencers_page = cards

influencer_network_page = html.Div([
    dash_echarts.DashECharts(
                        option = option_graph,
                        # events = events,
                        id='echarts_graph',
                        style={
                            "width": '100vw',
                            "height": '90vh',
                        },
                    )
])

def compare_radial(user1, user2):
    username1, total_avg_likes, total_avg_comments, total_avg_followers, total_avg_video_views, influencer_likes1, influencer_comments1, influencer_followers1, influencer_video_views1 = radial_data(user1)
    username2, _, _, _, _, influencer_likes2, influencer_comments2, influencer_followers2, influencer_video_views2 = radial_data(user2)

    option_radial = {
        'tooltip': {
            'trigger': 'item'
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left'
        },
        'radar': [
            {
            'indicator': [
                { 'text': 'Followers', 'max': 5 },
                { 'text': 'Likes', 'max': 5 },
                { 'text': 'Video Views', 'max': 5 },
                { 'text': 'Comments', 'max': 5 }
            ],
            'radius': 100,
            #   'center': ['50%', '60%']
            },
        ],
        'series': [
            {
            'type': 'radar',
            # 'tooltip': {
            #     'trigger': 'item'
            # },
            'data': [
                {
                'value': [total_avg_followers, total_avg_likes, total_avg_video_views, total_avg_comments],
                'name': 'Average',
                'itemStyle': {'color':'#AEB0AA'},
                'lineStyle': {'color':'#AEB0AA', 'type': 'dashed'},
                # 'areaStyle': {'color': '#AEB0AA'}
                },
                {
                'value': [influencer_followers1, influencer_likes1, influencer_video_views1, influencer_comments1],
                'name': username1,
                'itemStyle': {'color':'#FFC300'},
                'lineStyle': {'color':'#FFC300'},
                'areaStyle': {'color': '#FFC300'}
                },
                {
                'value': [influencer_followers2, influencer_likes2, influencer_video_views2, influencer_comments2],
                'name': username2,
                'itemStyle': {'color':'#ADD8E6'},
                'lineStyle': {'color':'#ADD8E6'},
                'areaStyle': {'color': '#ADD8E6'}
                }
            ], 
            'emphasis': {
                'itemStyle': {
                'shadowBlur': 10,
                'shadowOffsetX': 0,
                'shadowColor': 'rgba(0, 0, 0, 0.5)'
                }
            }
            },
        ]
        }
    return option_radial

comparison_page = html.Div(
    children=[
        html.H3("Compare Two Influencers", style={"margin-top": "30px", "text-align": "center"}), 
        html.Br(),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id="dropdown_1",
                        options=dropdown_options(),
                        value='_shinekoh',
                        style={"margin-left": "7px", "width": "97.8%"}
                        ),
                    html.Div(id="influencer-1"), 
                ]), 
                dbc.Col([
                    dcc.Dropdown(
                        id="dropdown_2",
                        options=dropdown_options(),
                        value='aglimpseofrach', 
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
    if compare_options > 0: 
        result = html.H3("choice 1 is " + str(dropdown_1) + " choice2 is " + str(dropdown_2))

        inf_df_1 = get_cur_infl_profile(dropdown_1)
        inf_df_2 = get_cur_infl_profile(dropdown_2)
        table1 = create_stats_table(inf_df_1)
        table2 = create_stats_table(inf_df_2)

        radial_layout = html.Div([
            
        ])

        comparison_layout = html.Div([
            html.Br(),
            html.H4("Results:", style={"margin-top": "30px", "text-align": "center"}), 
            html.Br(),
            dbc.Container([
                dbc.Row([
                    dbc.Col([table1]),
                    dbc.Col([table2]),
                ]),
                dbc.Row([
                    dbc.Col([dash_echarts.DashECharts(
                                option = compare_radial(dropdown_1, dropdown_2),
                                # events = events,
                                id='echarts_radar_compare',
                                style={
                                    "width": '35vw',
                                    "height": '35vh',
                                },)
                    ]),
                    dbc.Col([dash_echarts.DashECharts(
                                option = create_bar(dropdown_1, dropdown_2),
                                # events = events,
                                id='echarts_bar_compare',
                                style={
                                    "width": '50vw',
                                    "height": '35vh',
                                },)
                    ])
                ]),
                # 
            ])
        ])



        return comparison_layout