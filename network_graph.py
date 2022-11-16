import json
import dash
from dash import Dash 
from dash import html
import dash_echarts
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.LUX]
)

app.title = "Influ-Finder"
import json
f = open('inf_graph.json')
graph = json.load(f)

option_graph = {
    'tooltip': {},
    'series': [
      {
        'name': 'Coauthor Network',
        'type': 'graph',
        'layout': 'force',
        'data': graph['nodes'],
        'links': graph['links'],
        # 'categories': graph['categories'],
        'roam': True,
        'label': {
          'show': True,
          'position': 'right',
          'formatter': '{b}'
        },
        'labelLayout': {
          'hideOverlap': True
        },
        'scaleLimit': {
          'min': 0.4,
          'max': 100,
          'nodeScaleRatio': 0.2
        },
        'lineStyle': {
          'color': 'source',
          'curveness': 0.1
        },
        # 'force': {
        #   'repulsion': 10
        # }
      }
    ]
}
app.layout = html.Div(
    className="row", 
    children=[
        html.Div("Hello website"),
        dash_echarts.DashECharts(
          option = option_graph,
          # events = events,
          id='echarts_graph',
          style={
              "width": '100vw',
              "height": '90vh',
          },
      )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)