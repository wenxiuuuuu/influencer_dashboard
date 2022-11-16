# Dash components, html, and dash tables
from dash import dcc 
# Import Bootstrap components
import dash_bootstrap_components as dbc
from data import get_card_data, get_profile_data

from dash import Input, Output, State, html, callback 

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

def create_card(index):
    name, username, biography, num_followers, dp_path = get_card_data(index)

    card = dbc.Card(
        [
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardBody(
                                    [html.H4(name, className="card-title", style={"height": "26px", "overflow-x": "scroll", "overflow-y": "hidden", "overflow": "overlay"})]
                                    )
                                ), 
                            dbc.Col(dbc.CardBody(
                                    [html.H4(username, className="card-title", style={"text-align": "right"})]
                                )
                            ),
                            html.Hr()
                        ]
                    ), 
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardImg(
                                    src=dp_path,
                                    className="img-fluid rounded-start",
                                    # style = {"max-width": "180px", "max-height": "180px"}
                                ),
                                className="col-md-4",
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4("Biography"), 
                                        html.P(
                                            biography,
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
                                                        html.H5(str(num_followers), style={"text-align": "right"})
                                                    ) 
                                                ]
                                            ), 
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.H5("Avg Likes")
                                                    ),
                                                    dbc.Col(
                                                        html.H5(str(num_followers), style={"text-align": "right"})
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
                    className="g-0 d-flex align-items-center",
                    ),

                    dbc.Button("See more", value=index, id="open_fs", class_name="mt-auto", style={"align-self": "stretch", "width": "100%", "flex": "1 1 auto"}),
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
                        id="modal-fs",
                        fullscreen=True,
                    ),
                ]
            )
                    
    ],
    className="mb-3",
    style = {"margin": "30px", "maxWidth": "600px"}
    )
    return(card)

def create_profile(index): 
    index = int(index)
    name, username, biography, num_followers, dp_path, recent_post = get_profile_data(index)

    # creating table 
    table_header = [html.Thead(html.Tr([html.Th("Followers"), html.Th(str(num_followers))]))]
    row1 = html.Tr([html.Td("Followers"), html.Td(str(num_followers))])
    row2 = html.Tr([html.Td("Avg Likes"), html.Td("502")])
    row3 = html.Tr([html.Td("Avg Comments"), html.Td("89")])
    row4 = html.Tr([html.Td("Engagement Rate"), html.Td("63%")])
    table_body = [html.Tbody([row1, row2, row3, row4])]
    table = dbc.Table(table_header + table_body, bordered=True, hover=True, responsive=True)



    profile = html.Div(
        className='container-fluid', 
        children=[
            dbc.ModalHeader(dbc.ModalTitle(name + "'s Profile")),
            html.Div(
                [
                    html.H3("Basic Information", style={"margin-top": "15px"}),
                    dbc.Progress(value=33),

                    dbc.Row(
                        [
                            dbc.Col(
                                className='col', 
                                children = [

                                    html.H4("Biography", className='text-muted'), 
                                    html.P(biography), 

                                    html.H4("Top Categories", className="text-muted"), 
                                    create_listgroup(["Men Health", "Fitness", "Tech"]), 

                                    html.Br(), 

                                    html.H4("Collaborations", className='text-muted'), 
                                    create_listgroup(["gatsbysg", "thetinselrack", "byinviteonlystore"])
                                ]
                            ), 
                            dbc.Col(
                                className='col', 

                                children = [
                                    html.H4("Statistics", className='text-muted'), 
                                    table, 

                                    html.H4("Hashtags", className='text-muted'), 
                                    html.Div(hashtag_buttons(["movingrubber", "groomingtips", "hairstyling", "TrustBankSG", "RicolaSG"]))
                                    # hashtag_buttons(["movingrubber", "groomingtips", "hairstyling", "TrustBankSG", "RicolaSG"])
                                    # dbc.Button("#kjahsdkjasd", className="btn-hash", href="https://www.instagram.com/explore/tags/movingrubber/")
                                ]
                            ),
                            dbc.Col(
                                className='col', 
                                children =[
                                    html.H4("Recent Post", className='text-muted'),
                                    html.Iframe(src="https://www.instagram.com/p/" + recent_post + "/embed")
                                ]
                                

                            )
                        ]
                    ), 
                    html.H3("Visualisations", style={"margin-top": "15px"}),
                    dbc.Progress(value=70),

                    html.H3("Connections", style={"margin-top": "15px"}),
                    dbc.Progress(value=100),
                    
                ], 
            )
        ], 
        style={"overflow": "scroll"}
    )
    return profile 

# in case cannot return profile 
empty_div = html.Div("Influencer's profile cannot be found :(")

@callback(
    output=[Output("modal-fs", "is_open"), Output("modal-fs", "children")],
    inputs=Input("open_fs", "n_clicks"),
    state=[State("modal-fs", "is_open"), State("open_fs", "value")]
)
def toggle_modal(n, is_open, open_fs):
    if n:
        profile = create_profile(open_fs)
        return [(not is_open), profile]
    
    return [is_open, empty_div]