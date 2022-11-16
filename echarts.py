import json 
import dash_echarts

def create_pie_chart(data): 
    option_pie = {
        'tooltip': {
            'trigger': 'item'
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left'
        },
        'series': [
            {
            'type': 'pie',
            'radius': '50%',
            'data': data, 
            'emphasis': {
                'itemStyle': {
                'shadowBlur': 10,
                'shadowOffsetX': 0,
                'shadowColor': 'rgba(0, 0, 0, 0.5)'
                }
            }
            }
        ]
        }
    return option_pie


# radar chart 
def create_radar(): 
    option_radar = {
        'tooltip': {
            'trigger': 'item'
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left',
            'data': ['Influencer', 'Average']
        },
        'radar': {
            'indicator': [
            { 'name': 'Followers', 'max': 30000 },
            { 'name': 'Likes', 'max': 2000 },
            { 'name': 'Comments', 'max': 300 },
            { 'name': 'Engagement', 'max': 100 },
            { 'name': 'Sponsorships', 'max': 100 }
            ]
        },
        'series': [
            {
            'type': 'radar',
            'data': [
                {
                'value': [20770, 502, 89, 63, 78],
                'name': 'Influencer'
                },
                {
                'value': [15800, 730, 39, 42, 59],
                'name': 'Average'
                }
            ]
            }
        ]
        }
    return option_radar


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