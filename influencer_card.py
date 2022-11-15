# Dash components, html, and dash tables
from dash import dcc 
# Import Bootstrap components
import dash_bootstrap_components as dbc
from data import get_card_data

from dash import Input, Output, State, html
from dash import callback 


# modal = html.Div(
#         [
#             dbc.Button("See more", id="open-fs", style={"width": "570px", "text-align": "center", "margin": "auto"}),
#             dbc.Modal(
#                 [
#                     dbc.ModalHeader(dbc.ModalTitle("Fullscreen modal")),
#                     dbc.ModalBody("Wow this thing takes up a lot of space..."),
#                 ],
#                 id="modal-fs",
#                 fullscreen=True,
#             ),
#         ], 
#         style={"position": "absolute", "bottom": "5px", "margin": "20px"}
#     )


@callback(
    Output("modal-fs", "is_open"),
    Input("open-fs", "n_clicks"),
    State("modal-fs", "is_open"),
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open


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
                                            style={"position": "relative", "height": "120px", "overflow-y": "scroll", "overflow-x": "hidden", "overflow": "overlay"}
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

                    dbc.Button("See more", value=index, id="open-fs", class_name="mt-auto", style={"align-self": "stretch", "width": "100%", "flex": "1 1 auto"}),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Influencer Profile")),
                            html.Div(
                                [
                                    html.H4(name),
                                    html.Iframe(src="https://www.instagram.com/p/CkqAwI-hWJu/embed")
                                ]
                                
                            )
                        ],
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

