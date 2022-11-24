# # Dash components, html, and dash tables
# from dash import dcc     
# import dash_echarts
# from dash.exceptions import PreventUpdate
# from os import path
# import json

# # Import Bootstrap components
# import dash_bootstrap_components as dbc
# from data import get_card_data, get_profile_data

# from dash import Input, Output, State, html, callback 
# from echarts import option_graph, create_pie_chart, create_radar
# from dash import register_page


# def create_profile(index): 
#     index = int(index)
#     name, username, biography, num_followers, dp_path, recent_post, data_pie = get_profile_data(index)

#     # creating table 
#     table_header = [html.Thead(html.Tr([html.Th("Followers"), html.Th(str(num_followers))]))]
#     row1 = html.Tr([html.Td("Followers"), html.Td(str(num_followers))])
#     row2 = html.Tr([html.Td("Avg Likes"), html.Td("502")])
#     row3 = html.Tr([html.Td("Avg Comments"), html.Td("89")])
#     row4 = html.Tr([html.Td("Engagement Rate"), html.Td("63%")])
#     table_body = [html.Tbody([row1, row2, row3, row4])]
#     table = dbc.Table(table_header + table_body, bordered=True, hover=True, responsive=True)


#     profile = html.Div(
#         className='container-fluid', 
#         children=[
#             dbc.ModalHeader(dbc.ModalTitle(name + "'s Profile")),
#             html.Div(
#                 [
#                     html.H3("Basic Information", style={"margin-top": "15px"}),
#                     dbc.Progress(value=33),

#                     dbc.Row(
#                         [
#                             dbc.Col(
#                                 className='col', 
#                                 children = [

#                                     html.H4("Biography", className='text-muted'), 
#                                     html.P(biography), 

#                                     html.H4("Top Categories", className="text-muted"), 
#                                     create_listgroup(["Men Health", "Fitness", "Tech"]), 

#                                     html.Br(), 

#                                     html.H4("Collaborations", className='text-muted'), 
#                                     create_listgroup(["gatsbysg", "thetinselrack", "byinviteonlystore"])
#                                 ]
#                             ), 
#                             dbc.Col(
#                                 className='col', 

#                                 children = [
#                                     html.H4("Statistics", className='text-muted'), 
#                                     table, 

#                                     html.H4("Hashtags", className='text-muted'), 
#                                     html.Div(hashtag_buttons(["movingrubber", "groomingtips", "hairstyling", "TrustBankSG", "RicolaSG"]))
#                                 ]
#                             ),
#                             dbc.Col(
#                                 className='col', 
#                                 children =[
#                                     html.H4("Recent Post", className='text-muted'),
#                                     html.Iframe(src="https://www.instagram.com/p/" + recent_post + "/embed")
#                                 ]
#                             )
#                         ]
#                     ), 
#                     html.H3("Visualisations", style={"margin-top": "15px"}),
#                     dbc.Progress(value=70),

#                     html.Div([
#                         dbc.Row([
#                             dbc.Col(
#                                 className='col', 
#                                 children=[
#                                 html.H4("Type of Posts", className='text-muted'), 
#                                 # pie chart 
#                                 dash_echarts.DashECharts(
#                                     option = create_pie_chart(data_pie),
#                                     # events = events,
#                                     id='echarts_pie',
#                                     style={
#                                         "width": '40vw',
#                                         "height": '30vh',
#                                     },
#                                 ),
#                             ]), 
#                             dbc.Col(
#                                 className='col', 
#                                 children=[
#                                 html.H4("Compared with Average", className='text-muted'), 
#                                 dash_echarts.DashECharts(
#                                     option = create_radar(),
#                                     # events = events,
#                                     id='echarts_radar',
#                                     style={
#                                         "width": '40vw',
#                                         "height": '30vh',
#                                     },
#                                 ),

#                             ])
#                         ])
#                     ]),

                    

#                     html.H3("Connections", style={"margin-top": "15px"}),
#                     dbc.Progress(value=100),

#                     dash_echarts.DashECharts(
#                         option = option_graph,
#                         # events = events,
#                         id='echarts_graph',
#                         style={
#                             "width": '100vw',
#                             "height": '90vh',
#                         },
#                     )
                    
#                 ], 
#             )
#         ], 
#         style={"overflow": "scroll"}
#     )
#     return profile 
