import json
import dash_echarts
from data import radial_data, pie_data, get_post_infos
from mongodata import post_df
from collections import Counter
from datetime import datetime
from network_graph import get_data_indiv_network

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


f = open('data/inf_graph_colour.json')
graph = json.load(f)

option_graph = {
    'tooltip': {},
    'legend': [
      {
        'data': ['Fashion','Health/Wellness','Media','Food','Electronics','Education','Other','Business','For Good', 'External Related Influencer'],
        'padding': [5,10],
        'itemGap': 25,
        'backgroundColor': 'white'
      }
    ],
    'color': ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#adadad'],
    'series': [
      {
        'name': 'Influencer Network',
        'type': 'graph',
        'layout': 'force',
        'data': graph['nodes'],
        'links': graph['links'],
        'categories': graph['categories'],
        'roam': True,
        'label': {
          'show': True,
          'position': 'right',
        #   'formatter': '{b}'
        },
        'labelLayout': {
          'hideOverlap': True
        },
        'scaleLimit': {
          'min': 0.3,
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

def color_range(eng_rate): 
    if 0<=eng_rate<25: 
        return '#FF6E76'
    elif 25<=eng_rate<50: 
        return '#FDDD60'
    elif 50<=eng_rate<75: 
        return '#58D9F9'
    else:
        return '#7CFFB2'
        
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
                # 'color': '#FFC300',
                'color': color_range(eng_rate), 
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

def line_graph(username):
    comments = list(get_post_infos(username)['comments_over_time'])
    likes = list(get_post_infos(username)['likes_over_time'])
    # timestamp = [datetime.fromtimestamp(i).strftime("%m-%y") for i in list(get_post_infos(username)['timestamp'])]
    post_no = list(range(1,get_post_infos(username)['num_posts']+1))
    post_type = list(get_post_infos(username)['post_type'])
    option = {
        'tooltip': {
            'trigger': 'axis'
        },
        'legend': {
            'data': ['Likes', 'Comments'], 
            'left': '10'
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '3%',
            'containLabel': True
        },
        'toolbox': {
            'feature': {
            'saveAsImage': {}
            }
        },
        'xAxis': {
            'type': 'category',
            'boundaryGap': False,
            'data': post_no, 
            'axisTick': {
                'alignWithLabel': True
            }
        },
        'yAxis': [
            {
                'name': 'Likes',
                'type': 'value', 
                'axisAutoAlign': True,
                'axisLine': {
                    'lineStyle': {
                        'color': 'blue'
                    }
                }
            },
                {
                'name': 'Comments',
                'position': 'right',
                'type': 'value', 
                'axisAutoAlign': True,
                'axisLine': {
                    'lineStyle': {
                        'color': 'green'
                    }
                }, 
                'splitLine': {
                    'show': False
                }
            }
        ],
        'series': [
            {
                'name': 'Likes',
                'type': 'line',
                'data': likes, 
                'lineStyle': {
                    'color': 'blue'
                }
            },
            {
                'name': 'Comments',
                'type': 'line',
                'stack': 'Total',
                'data': comments, 
                'yAxisIndex': 1
            }
        ]
        }
    return option


# def indiv_network(username):
#     small_dict = get_data_indiv_network(username)
#     option_graph = {
#         'tooltip': {},
#         'series': [
#             {
#                 'name': f"{username}'s Network",
#                 'type': 'graph',
#                 'layout': 'force',
#                 'data': small_dict['nodes'],
#                 'links': small_dict['links'],
#                 'categories': small_dict['categories'],
#                 'roam': True,
#                 'label': {
#                     'show': True,
#                     'position': 'right',
#                     'formatter': '{b}'
#                 },
#                 'labelLayout': {
#                 '   hideOverlap': True
#                 },
#                 'scaleLimit': {
#                     'min': 0.4,
#                     'max': 100,
#                     'nodeScaleRatio': 0.2
#                 },
#                 'lineStyle': {
#                     'color': 'source',
#                     'curveness': 0.1
#                 },
#             }
#         ]
#     }
#     return