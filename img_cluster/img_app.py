import dash
from dash.exceptions import PreventUpdate
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Create dash app
app = dash.Dash(__name__)

# Set dog and cat images
# dogImage = "https://www.iconexperience.com/_img/v_collection_png/256x256/shadow/dog.png"
# dogImage = 'https://drive.google.com/file/d/13xUSrvk22XWnpi9wRadqYl_v1TrQxUxl/view?usp=share_link'
# dogImage = 'https://drive.google.com/uc?export=view&id=13xUSrvk22XWnpi9wRadqYl_v1TrQxUxl'
# catImage = "https://d2ph5fj80uercy.cloudfront.net/06/cat3602.jpg"

# # Generate dataframe
# df = pd.DataFrame(
#    dict(
#       x=[1, 2],
#       y=[2, 4],
#       images=[dogImage,catImage],
#    )
# )

img_df = pd.read_csv('../data/image_cluster_urls.csv')

# Create scatter plot with x and y coordinates
# fig = px.scatter(df, x="x", y="y",custom_data=["images"])
new_fig = px.scatter(img_df, x='1d', y='2d', custom_data=['img_url'], color='clusterid')

# Update layout and update traces
new_fig.update_layout(clickmode='event+select')
new_fig.update_traces(marker_size=10)

# Create app layout to show dash graph
app.layout = html.Div(
   [
      dcc.Graph(
         id="graph_interaction",
         figure=new_fig,
      ),
      html.Img(id='image', src='', style={'height':'25%', 'width':'25%'})
   ]
)

NUMBER_OF_TRACES = len(img_df['clusterid'].unique())


## we take the 4 closest points because the 1st closest point will be the point itself
def get_n_closest_points(x0, y0, df=img_df[['1d','2d']].copy(), n=4):

    """we can save some computation time by looking for the smallest distance^2 instead of distance"""
    """distance = sqrt[(x1-x0)^2 + (y1-y0)^2]"""
    """distance^2 = [(x1-x0)^2 + (y1-y0)^2]"""
    
    df["dist"] = (df["1d"]-x0)**2 + (df["2d"]-y0)**2

    ## we don't return the point itself which will always be closest to itself
    return df.sort_values(by="dist")[1:n][["1d","2d"]].values


# html callback function to hover the data on specific coordinates
@app.callback(
   Output('image', 'src'),
   Input('graph_interaction', 'hoverData'))
def open_url(hoverData):
   if hoverData:
      return hoverData["points"][0]["customdata"][0]
   else:
      raise PreventUpdate

@app.callback(
   Output('graph_interaction', 'figure'),
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
        # print("after\n")
        # print(figure['data'])
        return figure
if __name__ == '__main__':
   app.run_server(debug=True)