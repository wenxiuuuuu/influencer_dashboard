# Dash components, html, and dash tables
from dash import dcc
import dash_echarts
from os import path
import plotly.express as px

# Import Bootstrap components
import dash_bootstrap_components as dbc
from data import get_influencer_statistics, get_post_infos
from dash import Input, Output, State, html, callback 
from echarts import option_graph, create_pie_chart, create_radial, create_gauge, line_graph, indiv_network

from mongodata import influencer_df, get_cur_infl_profile, comments_df, subset_df, comments_user

# hyperlink for category
def create_listgroup(list):
    item_list = []
    for item in list:
        create_item = dbc.ListGroupItem(item, href="https://www.instagram.com/" + item[1:] + "/")
        item_list.append(create_item)
    return dbc.ListGroup(item_list)

def hashtag_buttons(list):
    hash_list = []
    for item in list:
        button = dbc.Button("#"+item, className="btn-hash", href="https://www.instagram.com/explore/tags/" + item)
        hash_list.append(button)
    return hash_list

def engagement_rate(current_influencer_df):
    num_followers = int(current_influencer_df['num_followers'].values)
    total_likes = int(current_influencer_df['avg_likes']) * 10
    total_comments = int(current_influencer_df['avg_comments']) * 10
    engagement = ((total_likes+total_comments)/num_followers)*100
    return round(engagement)

def create_card(username):
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
                    dbc.Modal(
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
    current_influencer_df = get_cur_infl_profile(username)

    # creating table
    row1 = html.Tr([html.Td("Followers"), html.Td(str(int(current_influencer_df['num_followers'].values)))])
    row2 = html.Tr([html.Td("Avg Likes"), html.Td(int(current_influencer_df['avg_likes']))])
    row3 = html.Tr([html.Td("Avg Comments"), html.Td(int(current_influencer_df['avg_comments']))])
    row4 = html.Tr([html.Td("Avg Video Views"), html.Td(int(current_influencer_df['avg_video_views']))])
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
                                    # create_listgroup(list(influencer_stats['category_counts'].keys())[:5]),
                                    create_listgroup(list({k: v for k, v in sorted(influencer_stats['category_counts'].items(), reverse=True, key=lambda item: item[1])}.keys())[:5]),

                                    html.Br(),

                                    html.H4("Top Collaborations", className='text-muted'),
                                    create_listgroup(['@' + x for x in influencer_stats['mentions'][:5]]),

                                    html.Br(),

                                    html.H4("Hashtags", className='text-muted'),
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
                                            option = create_gauge(engagement_rate(current_influencer_df)),
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
                                ]
                                ,
                                style={"box-sizing": 'border-box'}),
                            dbc.Col(
                                className='col',
                                children=[
                                        html.H4("Type of Posts", className='text-muted', style={'text-align':'center'}),
                                        dash_echarts.DashECharts(
                                            option = create_pie_chart(username),
                                            id='echarts_pie',
                                            style={
                                                # "width": '35vw',
                                                "height": '35vh',
                                            },
                                        )
                                ]
                                ),
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
                                html.H4("Likes & Comments", className='text-muted', style={'text-align':'center'}),
                                html.P("For recent posts", style={'text-align':'center'}),
                                dash_echarts.DashECharts(
                                            option = line_graph(username),
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
                    html.H3("First and Second Degree Connections", style={"margin-top": "15px"}),
                    dbc.Progress(value=100),
                    html.Br(),

                    dash_echarts.DashECharts(
                        option = indiv_network(username),
                        style={
                            "width": '73vw',
                            "height": '70vh',
                        },
                    )
                    
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
