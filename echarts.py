import json 
import dash_echarts
from data import radial_data, pie_data
from mongodata import post_df
from collections import Counter

def create_pie_chart(username): 
    data = pie_data(username)
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
def create_radial(username): 
    username, total_avg_likes, total_avg_comments, total_avg_followers, total_avg_video_views, influencer_likes, influencer_comments, influencer_followers, influencer_video_views = radial_data(username)
    option_radial = {
        'tooltip': {
            'trigger': 'item'
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left'
        },
        'radar': [
            {
            'indicator': [
                { 'text': 'Followers', 'max': 5 },
                { 'text': 'Likes', 'max': 5 },
                { 'text': 'Video Views', 'max': 5 },
                { 'text': 'Comments', 'max': 5 }
            ],
            'radius': 100,
            #   'center': ['50%', '60%']
            },
        ],
        'series': [
            {
            'type': 'radar',
            # 'tooltip': {
            #     'trigger': 'item'
            # },
            'data': [
                {
                'value': [total_avg_followers, total_avg_likes, total_avg_video_views, total_avg_comments],
                'name': 'Average',
                'itemStyle': {'color':'#AEB0AA'},
                'lineStyle': {'color':'#AEB0AA'},
                'areaStyle': {'color': '#AEB0AA'}
                },
                {
                'value': [influencer_followers, influencer_likes, influencer_video_views, influencer_comments],
                'name': username,
                'itemStyle': {'color':'#FFC300'},
                'lineStyle': {'color':'#FFC300'},
                'areaStyle': {'color': '#FFC300'}
                }
            ], 
            'emphasis': {
                'itemStyle': {
                'shadowBlur': 10,
                'shadowOffsetX': 0,
                'shadowColor': 'rgba(0, 0, 0, 0.5)'
                }
            }
            },
        ]
        }
    return option_radial


f = open('data/inf_graph.json')
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

def create_bar(user1, user2):
    user1_dict = Counter(post_df.loc[post_df['username']==user1]['post_type'])
    user2_dict =  Counter(post_df.loc[post_df['username']==user2]['post_type'])
    option_bar = {
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
                }
        },
        'legend': {},
        'grid': {
            'left': '5%',
            'right': '4%',
            'bottom': '3%',
            'containLabel': True
        },
        'xAxis': {
            'type': 'value'
        },
        'yAxis': {
            'type': 'category',
            'data': [user2, user1]
        },
        'series': [
            {
                'name': 'Sliding Images      ', # need space or else legend will overlap
                'type': 'bar',
                'stack': 'total',
                'label': {
                    'show': True
                },
                'emphasis': {
                    'focus': 'series'
                },
                'data': [user2_dict['GraphSidecar'], user1_dict['GraphSidecar']]
            },
            {
                'name': 'Single Image     ',
                'type': 'bar',
                'stack': 'total',
                'label': {
                    'show': True
                },
                'emphasis': {
                    'focus': 'series'
                },
                'data': [user2_dict['GraphImage'], user1_dict['GraphImage']]
            },
            {
                'name': 'Video',
                'type': 'bar',
                'stack': 'total',
                'label': {
                    'show': True
                },
                'emphasis': {
                    'focus': 'series'
                },
                'data': [user2_dict['GraphVideo'], user1_dict['GraphVideo']]
            },
        ]
    }
    return option_bar

def create_gauge(eng_rate):
    option_gauge = {
        'series': [
            {
            'type': 'gauge',
            'startAngle': 180,
            'endAngle': 0,
            'min': 0,
            'max': 100,
            'splitNumber': 10,
            'itemStyle': {
                'color': '#FFC300',
            },
            'progress': {
                'show': True,
                'roundCap': True,
                'width': 12
            },
            'pointer': {        # no pointer
                'icon': '',
                'length': '75%',
                'width': 0,
                'offsetCenter': [0, '5%']
            },
            'axisLine': {
                'roundCap': True,
                'lineStyle': {
                'width': 12
                }
            },
            'axisTick': {
                'splitNumber': 2,
                'lineStyle': {
                'width': 1,
                'color': '#999'
                }
            },
            'splitLine': {
                'length': 6,
                'lineStyle': {
                'width': 2,
                'color': '#999'
                }
            },
            'axisLabel': {
                'distance': 15,
                'color': '#999',
                'fontSize': 10
            },
            'title': {
                'show': False
            },
            'detail': {
                'formatter': '{value}%',
                'offsetCenter': [0, '-20%'],
                'valueAnimation': True,
                'fontSize': 20
            },
            'data': [
                {
                'value': eng_rate
                }
            ]
            }
        ]
    }
    return option_gauge