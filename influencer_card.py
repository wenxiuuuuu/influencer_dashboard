# Dash components, html, and dash tables
from dash import dcc     
import dash_echarts
from dash.exceptions import PreventUpdate
from os import path
import json
import pandas as pd
import plotly.express as px
import re

# Import Bootstrap components
import dash_bootstrap_components as dbc
from data import get_influencer_statistics, get_post_infos
from dash import Input, Output, State, html, callback 
from echarts import option_graph, create_pie_chart, create_radial, create_gauge, line_graph

from mongodata import influencer_df, get_cur_infl_profile, comments_df, subset_df, comments_user

# hyperlink for category
def create_listgroup(list):
    item_list = []
    for item in list: 
        create_item = dbc.ListGroupItem(item, href="https://www.instagram.com/" + item + "/")
        item_list.append(create_item)
    return dbc.ListGroup(item_list)

def hashtag_buttons(list): 
    hash_list = []
    for item in list: 
        button = dbc.Button("#"+item, className="btn-hash", href="https://www.instagram.com/explore/tags/" + item)
        hash_list.append(button)
    return hash_list

def engagement_rate(current_influencer_df, influencer_stats, username): 
    num_posts = int(get_post_infos(username)['num_posts'])
    num_followers = int(current_influencer_df['num_followers'].values)
    # total_likes = int(current_influencer_df['avg_likes']) * num_posts
    # total_comments = int(current_influencer_df['avg_comments']) * num_posts
    total_likes = int(current_influencer_df['avg_likes']) * 10
    total_comments = int(current_influencer_df['avg_comments']) * 10
    # avg_video_views = int(current_influencer_df['avg_video_views'])
    # no_collaborations = len(influencer_stats['mentions'])
    engagement = ((total_likes+total_comments)/num_followers)*100
    # engagement = ((avg_likes*5 + avg_comments*6 + avg_video_views*2 + no_collaborations*10)/num_followers)*100
    return round(engagement)


# data = {"Images": 17, "Sidecars": 13, "Videos": 20}
# datajson = json.dumps(data)

# def pie_chart(): 
#     option = "{ tooltip: {trigger: 'item'},legend: {top: '5%',left: 'center'},series: [{name: 'Access From',type: 'pie',radius: ['40%', '70%'],avoidLabelOverlap: false,itemStyle: {borderRadius: 10,borderColor: '#fff',borderWidth: 2},label: {show: false,position: 'center'},emphasis: {label: {show: true,fontSize: '40',fontWeight: 'bold'}},labelLine: {show: false},data: { value: 17, name: 'Images' },{ value: 13, name: 'Sidecars' },{ value: 20, name: 'Videos' }}]};"
#     return option 

def create_card(username):
    # name, username, biography, num_followers, dp_path = get_card_data(index)
    # name, username, biography, num_followers, dp_path, recent_post, avg_comments, avg_likes, avg_video_views, post_type, mentions, hashtags, category_counts = get_profile_data(username)
    current_influencer_df = get_cur_infl_profile(username)
    dp_path = '/assets/images/' + username + '.jpg'   

    card = dbc.Container([
        dbc.Card(
        [
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardBody(
                                    [html.H4(current_influencer_df['name'], className="card-title", style={"height": "26px", "overflow-x": "scroll", "overflow-y": "hidden", "overflow": "overlay"})]
                                    )
                                ), 
                            dbc.Col(dbc.CardBody(
                                    [html.H4('@' + username, className="card-title", style={"text-align": "right"})]
                                )
                            ),
                            html.Hr(style={'margin-top':'-1vw', 'margin-left': '0.8vw', 'width':'40vw'})
                        ]
                    ), 
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardImg(
                                    src=dp_path,
                                    className="img-fluid rounded-start",
                                    style = {"max-width": "180px", "min-height": "180px", 'border-radius': '50%'}
                                ),
                                className="col-md-4",
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4("Biography"), 
                                        html.P(
                                            current_influencer_df['biography'],
                                            className="card-text",
                                            style={"position": "relative", "height": "100px", "overflow-y": "scroll", "overflow-x": "hidden", "overflow": "overlay"}
                                        ),
                                        html.Hr(),
                                        html.Div([
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.H5("Followers")
                                                    ),
                                                    dbc.Col(
                                                        html.H5(str(int(current_influencer_df['num_followers'])), style={"text-align": "right"})
                                                    ) 
                                                ]
                                            ), 
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.H5("Avg Likes")
                                                    ),
                                                    dbc.Col(
                                                        html.H5(str(int(current_influencer_df['avg_likes'])), style={"text-align": "right"})
                                                    ) 
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.H5("Category"), width=5
                                                    ),
                                                    dbc.Col(
                                                        html.H5(str(current_influencer_df['category_name'].values[0]), style={"text-align": "right"}), width=7
                                                    ) 
                                                ]
                                            )
                                        ]
                                        )
                                    ]
                                ),
                                className="col-md-8",
                            ),
                        ],
                    className="g-0 d-flex align-items-center", style={'margin-top':'-1vw'}
                    ),

                    dbc.Button("See more", value=current_influencer_df['username_html'].values[0], id=f"open_fs{current_influencer_df['username_html'].values[0]}", class_name="mt-auto", style={"width": "100%"}),
                    # style={"align-self": "stretch", "width": "105%", "flex": "1 1 auto"}
                    dbc.Modal(
                        # [
                        #     dbc.ModalHeader(dbc.ModalTitle("Influencer Profile")),
                        #     html.Div(
                        #         [
                        #             html.H4(name),
                        #             html.Iframe(src="https://www.instagram.com/p/CkqAwI-hWJu/embed")
                        #         ]
                        #     )
                        # ],
                        id=f"modal-fs{current_influencer_df['username_html'].values[0]}",
                        # fullscreen=True,
                        scrollable=True,
                        size='xl',
                    ),
                ]
            )
        ])          
    ],
    className="mb-3",
    style = {"margin": "1vw", "maxWidth": "40vw", "padding": "0px"}
    )
    return card

def show_comments(username):
    if username in comments_user:
        # print(subset_df.loc[(subset_df['username']==username) & (subset_df['binary_class']=='POSITIVE')]['url'].values[0] + "embed")
        comments_layout = html.Div([
                html.H4("Comment Sentiment", className='text-muted', style={'text-align':'center'}), 
                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody(
                                [

                                    html.H5("Most Positive Comment", className="card-title"),
                                    html.Iframe(src=subset_df.loc[(subset_df['username']==username) & (subset_df['binary_class']=='POSITIVE')]['url'].values[0] + "embed",
                                        style={'maxHeight':'440px', 'maxWidth':'300px',}),
                                    # html.Br(),
                                    # html.Br(),
                                    html.P('"' + subset_df.loc[(subset_df['username']==username) & (subset_df['binary_class']=='POSITIVE')]['comments'] + '"', style={'text-align':'center'}),
                                ], style={'text-align':'center'}
                            ),
                        ),
                    ]),
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Least Positive Comment", className="card-title"),
                                    html.Iframe(src=subset_df.loc[(subset_df['username']==username) & (subset_df['binary_class']=='NEGATIVE')]['url'].values[0] + "embed",
                                        style={'maxHeight':'440px','maxWidth':'300px'}),
                                    html.P('"' + subset_df.loc[(subset_df['username']==username) & (subset_df['binary_class']=='NEGATIVE')]['comments'] + '"', style={'text-align':'center',}),
                                    # dbc.CardLink("Card link", href="#"),
                                    # dbc.CardLink("External link", href="https://google.com"),
                                ], style={'text-align':'center'}
                            ),
                        ),
                    ])
                ])
        ])
        return comments_layout
    else:
        return html.Div()


def create_profile(username): 
    # index = int(index)
    # name, username, biography, num_followers, dp_path, recent_post, avg_comments, avg_likes, avg_video_views, post_type, mentions, hashtags, category_counts = get_profile_data(index)
    current_influencer_df = get_cur_infl_profile(username)
    # data_pie = pie_data()

    # creating table 
    # table_header = [html.Thead(html.Tr([html.Th("Followers"), html.Th(str(num_followers))]))]
    row1 = html.Tr([html.Td("Followers"), html.Td(str(int(current_influencer_df['num_followers'].values)))])
    row2 = html.Tr([html.Td("Avg Likes"), html.Td(int(current_influencer_df['avg_likes']))])
    row3 = html.Tr([html.Td("Avg Comments"), html.Td(int(current_influencer_df['avg_comments']))])
    row4 = html.Tr([html.Td("Avg Video Views"), html.Td(int(current_influencer_df['avg_video_views']))])
    # row5 = html.Tr([html.Td("Engagement Rate"), html.Td("63%")])
    table_body = [html.Tbody([row1, row2, row3, row4])]
    table = dbc.Table(table_body, bordered=True, hover=True, responsive=True)

    # create sunburst 
    influencer_stats = get_influencer_statistics(username)
    sunburst_fig = px.sunburst(influencer_stats['username_cat_df'], path=['category', 'username'])

    profile = html.Div(
        className='container-fluid', 
        children=[
            dbc.ModalHeader(dbc.ModalTitle(current_influencer_df['name'] + "'s Profile")),
            html.Div(
                [
                    html.H3("Basic Information", style={"margin-top": "15px"}),
                    dbc.Progress(value=33),
                    html.Br(),

                    dbc.Row(
                        [
                            dbc.Col(
                                className='col', 
                                children = [

                                    html.H4("Top Categories of Brands Worked With", className="text-muted"), 
                                    # create_listgroup(["Men Health", "Fitness", "Tech"]), 
                                    # create_listgroup(list(influencer_stats['category_counts'].keys())[:5]), 
                                    create_listgroup(list({k: v for k, v in sorted(influencer_stats['category_counts'].items(), reverse=True, key=lambda item: item[1])}.keys())[:5]),

                                    html.Br(), 

                                    html.H4("Top Collaborations", className='text-muted'), 
                                    # create_listgroup(["gatsbysg", "thetinselrack", "byinviteonlystore"])
                                    create_listgroup(['@' + x for x in influencer_stats['mentions'][:5]]),

                                    html.Br(), 

                                    html.H4("Hashtags", className='text-muted'), 
                                    # html.Div(hashtag_buttons(["movingrubber", "groomingtips", "hairstyling", "TrustBankSG", "RicolaSG"]))
                                    html.Div(hashtag_buttons(influencer_stats['hashtags']))
                                ]
                            ), 
                            dbc.Col(
                                className='col', 

                                children = [

                                    html.H4("Biography", className='text-muted'), 
                                    html.P(current_influencer_df['biography']), 

                                    html.H4("Influencer's Category", className='text-muted'), 
                                    html.P(current_influencer_df['category_name']), 

                                    html.H4("Engagement Rate", className='text-muted'), 
                                    html.Div(dash_echarts.DashECharts(
                                            option = create_gauge(engagement_rate(current_influencer_df, influencer_stats, username)),
                                            # option = create_gauge('63'),  # engagement rate?
                                            # events = events,
                                            id='echarts_pie',
                                            style={
                                                # "width": '25vw',
                                                "height": '35vh',
                                            },
                                        ), style={'margin-top':'-2vh'}),

                                    html.H4("Statistics", className='text-muted', style={'margin-top':'-13vh'}), 
                                    table, 
                                ]
                            ),
                            dbc.Col(
                                className='col', 
                                children =[
                                    html.H4("Recent Post", className='text-muted'),
                                    html.Iframe(src="https://www.instagram.com/p/" + current_influencer_df['recent_pic_short'].values[0] + "/embed",
                                        style={'height':'780px'}),
            
                                ]
                            )
                        ]
                    ), 
                    html.Br(),
                    html.H3("Metrics", style={"margin-top": "15px"}),
                    dbc.Progress(value=70),
                    html.Br(),

                    dbc.Container([
                        dbc.Row([
                            dbc.Col(
                                className='col', 
                                children=[
                                    # dbc.Card([
                                        html.H4("Type of Posts", className='text-muted', style={'text-align':'center'}), 
                                        # pie chart 
                                        dash_echarts.DashECharts(
                                            option = create_pie_chart(username),
                                            # events = events,
                                            id='echarts_pie',
                                            style={
                                                # "width": '35vw',
                                                "height": '35vh',
                                            },
                                        )
                                    # ], style={"margin": "5px", "width": '30vw'},
                                # ),
                                ],
                                style={"box-sizing": 'border-box'}), 
                            dbc.Col(
                                className='col', 
                                children=[
                                    # dbc.Card([
                                        html.H4("Compared with Average", className='text-muted', style={'text-align':'center'}), 
                                        dash_echarts.DashECharts(
                                            option = create_radial(username),
                                            # events = events,
                                            id='echarts_radar',
                                            style={
                                                # "width": '35vw',
                                                "height": '35vh',
                                            },
                                        ),
                                    # ], style={"margin": "3px", "width": '30vw'}), 
                            ]), 
                            # dbc.Col(
                            #     className='col', 
                            #     ), 
                        ], style={'height':'35vh'}), 
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                    html.H4("All Brand Categories & Collaborators worked with", className='text-muted', style={'text-align':'center'}), 
                                    dcc.Graph(figure=sunburst_fig, 
                                        style={
                                            # "width": '100vw', 
                                            'justifyContent':'center',
                                            'align-items':'center',
                                            'display': 'flex', 
                                        },)
                            ]),

                            dbc.Col([
                                html.H4("Likes & Comments over Time", className='text-muted', style={'text-align':'center'}), 
                                html.P("For each post"),
                                # html.H5('add another graph here..?'), 
                                dash_echarts.DashECharts(
                                            option = line_graph(username),
                                            # events = events,
                                            id='likes_comments',
                                            style={
                                                # "width": '35vw',
                                                "height": '40vh',
                                            },
                                        ),
                            ])
                        ]),

                        dbc.Row([show_comments(username)])
                    ]),

                    
                    html.Br(),
                    html.H3("Connections", style={"margin-top": "15px"}),
                    dbc.Progress(value=100),
                    html.Br(),

                    # dash_echarts.DashECharts(
                    #     option = option_graph,
                    #     # events = events,
                    #     id='echarts_graph',
                    #     style={
                    #         "width": '100vw',
                    #         "height": '90vh',
                    #     },
                    # )
                    
                ], 
            )
        ], 
        style={"overflow": "scroll"}
    )
    return profile 

# in case cannot return profile 
empty_div = html.Div("Influencer's profile cannot be found :(")


def toggle_modal(n, is_open, open_fs):
    # print(n, is_open, open_fs)
    if n:
        open_fs_new = influencer_df.loc[influencer_df['username_html']==open_fs]['username'].values[0]
        profile = create_profile(open_fs_new)
        return [(not is_open), profile]
    
    return [is_open, empty_div]
for i in influencer_df['username_html']:
    # username_html = pattern.sub('', i)
    callback(
        output=[Output(f"modal-fs{i}", "is_open"), Output(f"modal-fs{i}", "children")],
        inputs=Input(f"open_fs{i}", "n_clicks"),
        state=[State(f"modal-fs{i}", "is_open"), State(f"open_fs{i}", "value")]
    )(toggle_modal)