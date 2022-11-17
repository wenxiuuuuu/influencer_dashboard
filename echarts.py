import json 
import dash_echarts
from data import radial_data

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
def create_radial(index): 
    username, total_avg_likes, total_avg_comments, total_avg_followers, total_avg_video_views, influencer_likes, influencer_comments, influencer_followers, influencer_video_views = radial_data(index)
    option_radial = {
        'title': {
            'text': 'Multiple Radar'
        },
        'tooltip': {
            'trigger': 'axis'
        },
        'legend': {
            'left': 'center',
            'data': [
            'A Phone',
            'Another Phone',
            ]
        },
        'radar': [
            {
            'indicator': [
                { 'text': 'Followers', 'max': 5 },
                { 'text': 'Avg Likes', 'max': 5 },
                { 'text': 'Avg Video Views', 'max': 5 },
                { 'text': 'Avg Comments', 'max': 5 }
            ],
            'radius': 100,
            #   'center': ['50%', '60%']
            },
        ],
        'series': [
            {
            'type': 'radar',
            'tooltip': {
                'trigger': 'item'
            },
            'areaStyle': {},
            'data': [
                {
                'value': [total_avg_followers, total_avg_likes, total_avg_video_views, total_avg_comments],
                'name': 'Average'
                },
                {
                'value': [influencer_followers, influencer_likes, influencer_video_views, influencer_comments],
                'name': username
                }
            ]
            },
        ]
        }
    return option_radial


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