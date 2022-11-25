# Dash components, html, and dash tables
from dash import html, dcc, Input, Output, State, callback
from dash.exceptions import PreventUpdate
# Import Bootstrap components
import dash_bootstrap_components as dbc
# from data import get_filtered_influ_df, rank_filtered_df
from influencer_card import create_card
# from data import dropdown_options
from data import *
from mongodata import influencer_df, post_df
import pandas as pd
import dash_echarts
from echarts import option_graph, create_bar
import plotly.express as px

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


unique_categories = influencer_df['top_category'].unique()
sort_layout = dbc.Container([
        dbc.Row([dbc.Col(dbc.InputGroup(
                        [   dbc.InputGroupText(html.I(className="fa fa-unsorted")),
                            dbc.InputGroupText("Sort by:"),
                            dbc.Select(options=[
                                {"label": "Username", "value": "username"},
                                {"label": 'Name', "value": 'name'},
                                {"label": "Followers", "value": 'num_followers'},
                                {"label": 'Avg Likes', "value": 'avg_likes'},
                            ], id='sort-dropdown', value='username')
                        ]), style={'margin-top':'0.28vw', "margin-left": "1vw"}),
                dbc.Col(dbc.Checklist(options=[{"label":'Ascending', "value":1}], value=[1], switch=True, id='sort-asc',style={"margin-left":"2vw", "margin-top":'1vw', 'border-radius': '50%'})),
                dbc.Col(html.Div([dbc.Input(id="input", placeholder="Search Influencers by Username...", type="text")], style={'width': "20vw", "margin-left":"5vw", "margin-top":"0.5vw"}),)
                ], style={'width':'90vw'}),

            # filter by category
        dbc.Row(dbc.InputGroup([
                dbc.InputGroupText(html.I(className="fa fa-filter"), style={'height':'36px'}),
                dbc.InputGroupText("Category:", style={'height':'36px'}),
                dcc.Dropdown(
                    unique_categories,
                    id="interest-input",
                    # multi=True,
                    style={'border-top-left-radius':'0px', 'border-bottom-left-radius':'0px', 'width':'30vw'}
                ),
            ],style={"margin-left":"1vw", "margin-top":'0.7vw'})),
        # className="g-0",
        html.Br(),
        html.Div(id='page-1-content')
    ],style={"margin-top":"2vw"})

@callback(Output('page-1-content', 'children'),
              [Input('input', 'value'), Input('sort-dropdown', 'value'), Input('sort-asc', 'value'), Input('interest-input', 'value')])
def page_1_dropdown(input, sortby, sort_asc, interest_input, ):
    temp = influencer_df.copy()
    if interest_input:
        temp = influencer_df[influencer_df['top_category'].isin([interest_input])].reset_index(drop=True)
    if len(sort_asc) == 1:
        asc = True
    else:
        asc = False
    temp = temp.sort_values(sortby, ascending=asc).reset_index(drop=True)
    if input:
        temp = temp.loc[temp['username'].str.contains(f"(?i){input}")].reset_index(drop=True)
    # return dash_table.DataTable(temp.to_dict('records'), [{"name": i, "id": i} for i in temp.columns])
    # return f"{df['Full Name'][0]}, {temp['Full Name'][0]}"
    row = []
    for i in temp['username']:
        row.append(create_card(i))

    influencers_page = dbc.Container(dbc.Row(row, style={"display": "flex", "align-items": "center", "justify-content": "center"}))

    num_results = html.P([html.Strong(f'{len(temp)}'), html.Span(' results returned.')], style={'text-align':'right','margin-right':'1.3vw'})
    return num_results, influencers_page

# # influencer page
# row = []
# for i in influencer_df['username']:
#     row.append(create_card(i))

# cards = dbc.Container(dbc.Row(row, style={"display": "flex", "align-items": "center", "justify-content": "center"}))
# influencers_page = cards

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

def create_table(inf_df_1, inf_df_2):
    table_header = [html.Thead(html.Tr([html.Th("Metrics"), html.Th(inf_df_1['username']), html.Th(inf_df_2['username'])]))]
    row1 = html.Tr([html.Td("Followers"), html.Td(str(int(inf_df_1['num_followers'].values))), html.Td(str(int(inf_df_2['num_followers'].values)))])
    row2 = html.Tr([html.Td("Avg Likes"), html.Td(int(inf_df_1['avg_likes'])), html.Td(int(inf_df_2['avg_likes']))])
    row3 = html.Tr([html.Td("Avg Comments"), html.Td(int(inf_df_1['avg_comments'])), html.Td(int(inf_df_2['avg_comments']))])
    row4 = html.Tr([html.Td("Avg Video Views"), html.Td(int(inf_df_1['avg_video_views'])), html.Td(int(inf_df_2['avg_video_views']))])
    row5 = html.Tr([html.Td("Engagement Rate"), html.Td("63%"), html.Td("63%")])
    table_body = [html.Tbody([row1, row2, row3, row4, row5])]
    table = dbc.Table(table_header + table_body, bordered=True, hover=True, responsive=True, style={'text-align':'center', 'justifyContent':'center', 'align-items':'center'})

    return table

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

        radial_layout = html.Div([

        ])

        comparison_layout = html.Div([
            html.Br(),
            html.H4("Results:", style={"margin-top": "30px", "text-align": "center"}),
            html.Br(),
            dbc.Container([
                dbc.Row([create_table(inf_df_1, inf_df_2)]),
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


img_df = pd.read_csv('data/image_cluster_urls.csv')
img_df['clusterid'] = img_df['clusterid'].astype('category')

# Create scatter plot with x and y coordinates
imgcluster_fig = px.scatter(
    img_df, x='1d', y='2d',
    custom_data=['img_url'],
    color='clusterid')

# Update layout and update traces
imgcluster_fig.update_layout(
    clickmode='event+select',
    xaxis=dict(showgrid=False, showticklabels=False, visible = False),
    yaxis=dict(showgrid=False, showticklabels=False, visible = False),
    plot_bgcolor = "white",
    legend_title_text='Cluster ID'
    )
imgcluster_fig.update_traces(marker_size=10)

cluster_page = html.Div(
   [
        html.H3("Which posts are similar?", style={"margin-top": "30px", "text-align": "center"}),
        html.H4("Choose category"),
        html.Div([
        dcc.Dropdown(
                        id="category_image",
                        options=[
                            {"label": "Fashion", "value": "fashion"},
                            {"label": "Health", "value": "health"},
                            # {"label": "Clothing (Brand)", "value": "Clothing (Brand)"},
                            # {"label": "Actor", "value": "Actor"},
                            # {"label": "Jewelry/watches", "value": "Jewelry/watches"},
                            # {"label": "Food & beverage", "value": "Food & beverage"},
                            ],
                        value = 'fashion',

                        ),
        ],style={'width': '20%', 'text-align': 'center'}),
        html.Br(),
        html.P('These images below are the central images of 5 clusters:', style={"text-align": "center"}),
        html.Br(),
        dbc.Container([
            dbc.Row([
                html.Img(
                    id='centroid_1_img',
                    src=img_df[(img_df['centroid']==1) & (img_df['clusterid']==0)]['img_url'].iloc[0],
                    style={'height':'280px', 'width':'260px'}),
                    # style={'height':'20%', 'width':'20%'}),
                html.Img(
                    id='centroid_2_img',
                    src=img_df[(img_df['centroid']==1) & (img_df['clusterid']==1)]['img_url'].iloc[0],
                    style={'height':'280px', 'width':'260px'}),
                html.Img(
                    id='centroid_3_img',
                    src=img_df[(img_df['centroid']==1) & (img_df['clusterid']==2)]['img_url'].iloc[0],
                    style={'height':'280px', 'width':'260px'}),
                html.Img(
                    id='centroid_4_img',
                    src=img_df[(img_df['centroid']==1) & (img_df['clusterid']==3)]['img_url'].iloc[0],
                    style={'height':'280px', 'width':'260px'}),
                html.Img(
                    id='centroid_5_img',
                    src=img_df[(img_df['centroid']==1) & (img_df['clusterid']==4)]['img_url'].iloc[0],
                    style={'height':'280px', 'width':'260px'}),
            ]),

            html.Br(),
            html.Br(),
            html.P('The cluster plot in 2D:', style={"text-align": "center"}),
            # html.Br(),
            dbc.Row([
                dbc.Col([
                    html.I('Click on any points below to see the image and its 5 most similar images.', style={"text-align": "center"}),
                    dcc.Graph(
                        id="graph_interaction",
                        figure=imgcluster_fig,
                        style={"border":"1px black solid",}
                        # "margin-left": "15px", "margin-right": "15px",
                        # "margin-top": "15px", "margin-bottom": "15px"}
                    ),
                ]),

                dbc.Col([html.Div(id='hover_cluster_name'),]),
            ])

        ]),

    #   html.Img(id='hover_image', src='', style={'height':'40%', 'width':'40%',}),
    #   html.Div("Other Neighbouring Images"),
    #   html.Img(id='neighbour_img_1', src='', style={'height':'20%', 'width':'20%'}),
    #   html.Img(id='neighbour_img_2', src='', style={'height':'20%', 'width':'20%'}),
    #   html.Img(id='neighbour_img_3', src='', style={'height':'20%', 'width':'20%'}),
    #   html.Img(id='neighbour_img_4', src='', style={'height':'20%', 'width':'20%'}),
    #   html.Img(id='neighbour_img_5', src='', style={'height':'20%', 'width':'20%'}),
   ]
)

NUMBER_OF_TRACES = len(img_df['clusterid'].unique())


## we take the n closest points because the 1st closest point will be the point itself
def get_n_closest_points(x0, y0, n=5, df=img_df[['1d','2d']].copy()):

    """we can save some computation time by looking for the smallest distance^2 instead of distance"""
    """distance = sqrt[(x1-x0)^2 + (y1-y0)^2]"""
    """distance^2 = [(x1-x0)^2 + (y1-y0)^2]"""
    n += 1
    df["dist"] = (df["1d"]-x0)**2 + (df["2d"]-y0)**2

    ## we don't return the point itself which will always be closest to itself
    return df.sort_values(by="dist")[1:n][["1d","2d"]].values


# html callback function to hover the data on specific coordinates
# @callback(
#    [Output('hover_image', 'src'),
#    Output('hover_cluster_name', 'children')
#    ],
#    Input('graph_interaction', 'hoverData'))
# def open_url(hoverData):
#    if hoverData:
#       cluster = img_df.iloc[hoverData["points"][0]['pointIndex']]['clusterid']
#       text = f'Cluster Number : {cluster}'
#       return hoverData["points"][0]["customdata"][0], text
#    else:
#       raise PreventUpdate



######################## KNN ########################
# @callback(
#    [Output('graph_interaction', 'figure'),
#    Output('neighbour_img_1', 'src'),
#    Output('neighbour_img_2', 'src'),
#    Output('neighbour_img_3', 'src'),
#    Output('neighbour_img_4', 'src'),
#    Output('neighbour_img_5', 'src')],
#    [Input('graph_interaction', 'clickData'),
#    Input('graph_interaction', 'figure')]
#    )
@callback(
    [Output('graph_interaction', 'figure'), Output('hover_cluster_name', 'children')],
    [Input('graph_interaction', 'clickData'), Input('graph_interaction', 'figure')]
)
def display_hover_data(clickData, figure):

    # print('clickdata',clickData)
    # print('figure',figure)
    # if clickData is None:
    #     # print("nothing was clicked")
    #     return figure
    # else:
    if clickData:
        hover_x, hover_y = clickData['points'][0]['x'], clickData['points'][0]['y']

        closest_points = get_n_closest_points(hover_x, hover_y)
        # print(closest_points)

        ## this means that this function has ALREADY added another trace, so we reduce the number of traces down the original number
        if len(figure['data']) > NUMBER_OF_TRACES:
            # print(f'reducing the number of traces to {NUMBER_OF_TRACES}')
            figure['data'] = figure['data'][:NUMBER_OF_TRACES]
            # print(figure['data'])

        new_traces = [{
            'marker': {'color': 'teal', 'symbol': 'circle'},
            'mode': 'markers',
            'orientation': 'v',
            'showlegend': False,
            'x': [x],
            'xaxis': 'x',
            'y': [y],
            'yaxis': 'y',
            'type': 'scatter',
            'selectedpoints': [0],
            # 'customdata':[]
        } for x,y in closest_points]

        figure['data'].extend(new_traces)

        # get the n images
        # loop it
        selected_img = img_df[ (img_df['1d']==clickData['points'][0]['x']) & (img_df['2d']==clickData['points'][0]['y'])] ['img_url'].iloc[0]
        img1 = img_df[(img_df['1d']==closest_points[0][0]) & (img_df['2d']==closest_points[0][1])]['img_url'].iloc[0]
        img2 = img_df[(img_df['1d']==closest_points[1][0]) & (img_df['2d']==closest_points[1][1])]['img_url'].iloc[0]
        img3 = img_df[(img_df['1d']==closest_points[2][0]) & (img_df['2d']==closest_points[2][1])]['img_url'].iloc[0]
        img4 = img_df[(img_df['1d']==closest_points[3][0]) & (img_df['2d']==closest_points[3][1])]['img_url'].iloc[0]
        img5 = img_df[(img_df['1d']==closest_points[4][0]) & (img_df['2d']==closest_points[4][1])]['img_url'].iloc[0]

        click_layout = html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.P('Selected Image:', style={"text-align":'center', "align-items": "center", "justify-content": "center"}),
                        html.Img(id='hover_image', src=selected_img, style={'height':'280px', 'width':'260px','margin-left':'1vw',}),
                    ]),
                    dbc.Col([
                        html.P("Other Neighbouring Images:", style={"text-align":'center', "align-items": "center", "justify-content": "center"}),
                        dbc.Carousel(
                            items=[
                                {"key": "1", "src": img1, "img_style":{'height':'280px', 'width':'260px'}},
                                {"key": "2", "src": img2, "img_style":{'height':'280px', 'width':'260px'}},
                                {"key": "3", "src": img3, "img_style":{'height':'280px', 'width':'260px'}},
                                {"key": "4", "src": img4, "img_style":{'height':'280px', 'width':'260px'}},
                                {"key": "5", "src": img5, "img_style":{'height':'280px', 'width':'260px'}}
                            ],
                            controls=True,
                            indicators=True,
                            style={'height':'80%', 'width':'80%', 'margin-left':'2vw'}
                        )
                    ]),
                ],)
            ])
        ])
        # return figure, img1, img2, img3, img4, img5
        return figure, click_layout
    raise PreventUpdate
