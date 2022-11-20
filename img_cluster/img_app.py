import dash
from dash.exceptions import PreventUpdate
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


# Create dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX],
    )


img_df = pd.read_csv('../data/image_cluster_urls.csv')
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

# Create app layout to show dash graph
app.layout = html.Div(
   [
      html.Div(
        children = [
            html.Img(
                id='centroid_1_img', 
                src=img_df[(img_df['centroid']==1) & (img_df['clusterid']==0)]['img_url'].iloc[0], 
                style={'height':'20%', 'width':'20%'}),
            html.Img(
                id='centroid_2_img', 
                src=img_df[(img_df['centroid']==1) & (img_df['clusterid']==1)]['img_url'].iloc[0], 
                style={'height':'20%', 'width':'20%'}),
            html.Img(
                id='centroid_3_img', 
                src=img_df[(img_df['centroid']==1) & (img_df['clusterid']==2)]['img_url'].iloc[0], 
                style={'height':'20%', 'width':'20%'}),
            html.Img(
                id='centroid_4_img', 
                src=img_df[(img_df['centroid']==1) & (img_df['clusterid']==3)]['img_url'].iloc[0], 
                style={'height':'20%', 'width':'20%'}),
            html.Img(
                id='centroid_5_img', 
                src=img_df[(img_df['centroid']==1) & (img_df['clusterid']==4)]['img_url'].iloc[0], 
                style={'height':'20%', 'width':'20%'}),
        ]
      ),
      dcc.Graph(
         id="graph_interaction",
         figure=imgcluster_fig,
         style={"border":"1px black solid",
         "margin-left": "15px", "margin-right": "15px",
         "margin-top": "15px", "margin-bottom": "15px"}
      ),
      html.Div(id='hover_cluster_name' ),
      html.Img(id='hover_image', src='', style={'height':'40%', 'width':'40%',}),
      html.Div("Other Neighbouring Images"),
      html.Img(id='neighbour_img_1', src='', style={'height':'20%', 'width':'20%'}),
      html.Img(id='neighbour_img_2', src='', style={'height':'20%', 'width':'20%'}),
      html.Img(id='neighbour_img_3', src='', style={'height':'20%', 'width':'20%'}),
      html.Img(id='neighbour_img_4', src='', style={'height':'20%', 'width':'20%'}),
      html.Img(id='neighbour_img_5', src='', style={'height':'20%', 'width':'20%'}),
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
@app.callback(
   [Output('hover_image', 'src'), 
   Output('hover_cluster_name', 'children')
   ],
   Input('graph_interaction', 'hoverData'))
def open_url(hoverData):
   if hoverData:
      cluster = img_df.iloc[hoverData["points"][0]['pointIndex']]['clusterid']
      text = f'Cluster Number : {cluster}'
      return hoverData["points"][0]["customdata"][0], text
   else:
      raise PreventUpdate


# html.Img(id='neighbour_img_1', src='', style={'height':'25%', 'width':'25%'}),
#       html.Img(id='neighbour_img_2', src='', style={'height':'25%', 'width':'25%'}),
#       html.Img(id='neighbour_img_3', src='', style={'height':'25%', 'width':'25%'}),
#       html.Img(id='neighbour_img_4', src='', style={'height':'25%', 'width':'25%'}),
#       html.Img(id='neighbour_img_5', src='', style={'height':'25%', 'width':'25%'}),
# 
######################## KNN ########################
@app.callback(
   [Output('graph_interaction', 'figure'), 
   Output('neighbour_img_1', 'src'), 
   Output('neighbour_img_2', 'src'),
   Output('neighbour_img_3', 'src'),
   Output('neighbour_img_4', 'src'),
   Output('neighbour_img_5', 'src')],
   [Input('graph_interaction', 'clickData'), 
   Input('graph_interaction', 'figure')]
   )
def display_hover_data(clickData, figure):
    print(clickData)
    if clickData is None:
        # print("nothing was clicked")
        return figure
    else:
        hover_x, hover_y = clickData['points'][0]['x'], clickData['points'][0]['y']
        closest_points = get_n_closest_points(hover_x, hover_y)
        print(closest_points)

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
        img1 = img_df[(img_df['1d']==closest_points[0][0]) & (img_df['2d']==closest_points[0][1])]['img_url'].iloc[0]
        img2 = img_df[(img_df['1d']==closest_points[1][0]) & (img_df['2d']==closest_points[1][1])]['img_url'].iloc[0]
        img3 = img_df[(img_df['1d']==closest_points[2][0]) & (img_df['2d']==closest_points[2][1])]['img_url'].iloc[0]
        img4 = img_df[(img_df['1d']==closest_points[3][0]) & (img_df['2d']==closest_points[3][1])]['img_url'].iloc[0]
        img5 = img_df[(img_df['1d']==closest_points[4][0]) & (img_df['2d']==closest_points[4][1])]['img_url'].iloc[0]
        return figure, img1, img2, img3, img4, img5
if __name__ == '__main__':
   app.run_server(debug=True)