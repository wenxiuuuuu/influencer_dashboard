import json
from data import radial_data, pie_data, get_post_infos
from mongodata import post_df, influencer_df
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


# radial chart
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
        return '#CC6155'
    elif 25<=eng_rate<50: 
        return '#ED820E'
    elif 50<=eng_rate<75: 
        return '#F5CB62'
    else:
        return '#7BCABB'
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
                'axisLine': {
                    'show': True,
                    'roundCap': True,
                    'lineStyle': {
                    'width': 12
                    }
                },
                'axisTick': {
                    'show': False
                },
                'splitLine': {
                    'show': False,
                    'length': 6,
                    'lineStyle': {
                    'width': 2,
                    'color': '#999'
                    }
                },
                'axisLabel': {
                    'show': False,
                    'distance': 15,
                    'color': '#999',
                    'fontSize': 10
                },
                'pointer': {
                    'show': False
                },
                'title': {
                    'show': False
                },
                'detail': {
                    'formatter': '{value}%',
                    'offsetCenter': [0, '-20%'],
                    'valueAnimation': True,
                    'fontSize': 20, 
                    'color': '#999'
                },
                'data': [
                    {
                    'value': eng_rate
                    }
                ]
            }, 
            {
                'type': 'gauge',
                'startAngle': 180,
                'endAngle': 0,
                'min': 0,
                'max': 100,
                'itemStyle': {
                    'color': color_range(eng_rate), 
                },
                'progress': {
                    'show': True,
                    'width': 0, 
                },
                'pointer': {
                    'show': False
                },
                'axisLine': {
                    'show': False, 
                    'lineStyle': {
                    'width': 6,
                    'color': [
                        [0.25, '#CC6155'],
                        [0.5, '#ED820E'],
                        [0.75, '#F5CB62'],
                        [1, '#7BCABB']
                    ]
        }
                },
                'axisTick': {
                    'show': True, 
                    'splitNumber': 2,
                    'lineStyle': {
                    'width': 1,
                    'color': 'auto'
                    }
                },
                'splitLine': {
                    'show': True, 
                    'length': 8,
                    'lineStyle': {
                    'width': 2,
                    'color': 'auto'
                    }
                },
                'axisLabel': {

                    'distance': 15,
                    'color': '#999',
                    'fontSize': 10
                },
                'detail': {
                    'show': False
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
    post_no = list(range(1,get_post_infos(username)['num_posts']+1))
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

f = open('data/unique_authors_dict_saved.json')
unique_authors_dict = json.load(f)

present_author_dict ={}
for k in list(influencer_df['username']):
    try:
        present_author_dict[k] = unique_authors_dict[k]
    except:
        continue

def convert(node, link, username):
    id_mapper = {}
    new_nodes = []
    new_links = []

    for idx, n in enumerate(node):
        cur_id = n['id']
        id_mapper[cur_id] = idx
        new_n = n.copy()
        new_n['id'] = idx
        # if n['name']==username:
        #     n['symbolSize']=20
        new_nodes.append(new_n)

    for e in link:
        new_source = id_mapper[e['source']]
        new_target = id_mapper[e['target']]
        new_e = e.copy()
        new_e['source'] = new_source
        new_e['target'] = new_target
        new_links.append(new_e)
    return new_nodes, new_links

def indiv_network(username):
    username_id = graph['nodes'][present_author_dict[username]]['id']

    # get first degree connections
    subset_links = []
    for i in graph['links']:
        if (i['target']==username_id) or (i['source']==username_id):
            subset_links.append(i)

    # get first degree nodes
    total = [username_id]
    for j in subset_links:
        if j['source'] not in total:
            total.append(j['source'])
        if j['target'] not in total:
            total.append(j['target'])

    # get all links
    final_links = []
    for i in graph['links']:
        if (i['target'] in total) or (i['source'] in total):
            final_links.append(i)

    # get all nodes
    all_nodes = set()
    for i in final_links:
        all_nodes.add(i['source'])
        all_nodes.add(i['target'])
    
    small_dict = {'categories':[{'name': "Fashion"}, {'name': "Health/Wellness"}, {'name': "Media"},{'name': "Food"},{'name': "Electronics"},{'name': "Education"},{'name': "Other"},{'name': "Business"},{'name': "For Good"},{'name': "External Related Influencer"}]}

    # small_dict['links'] = final_links
    # small_dict['nodes'] = [big_dict['nodes'][i] for i in all_nodes]

    small_dict['links'] = final_links
    small_dict['nodes'] = [graph['nodes'][i] for i in all_nodes]
    new_node, new_link = convert(small_dict['nodes'], small_dict['links'], username)

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
        'name': f"{username}'s network",
        'type': 'graph',
        'layout': 'force',
        'data': new_node,
        'links': new_link,
        # 'data': [{'id': 10, 'name': 'aglimpseofrach', 'draggable': True, 'category': 2}, {'id': 100, 'name': 'xianwenpoops', 'draggable': True, 'category': 2}],
        # 'links': [{'source': 10, 'target': 100, 'lineStyle': {'color': '#D3D3D3'}},],
        'categories': small_dict['categories'],
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
      }
    ]
}
    return option_graph
