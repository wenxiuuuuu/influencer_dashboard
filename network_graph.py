import ast
import json

from mongodata import influencer_df
from constants import CATEGORY_DICT

# for i,j in enumerate(influencer_df['related_influencers']):
#     influencer_df['related_influencers'][i] = ast.literal_eval(j)
# influencer_df = influencer_df.drop_duplicates(subset=['name','biography'],keep='last').reset_index(drop=True)

# # drop rows with no related influencers
# influencer_df['len_related'] = influencer_df['related_influencers'].apply(lambda x: len(x))
# drop_index = influencer_df.loc[influencer_df['len_related']==0].index
# influencer_df = influencer_df.drop(index=drop_index).reset_index(drop=True)

# # take top 10 related influencers
# influencer_df['related_25'] = influencer_df['related_influencers'].apply(lambda x: x[:10])

# # give each author a unique id
# all_authors = list(influencer_df['username'])
# for i in influencer_df['related_25']:
#     all_authors.extend(i)
# unique_authors_list = list(set(all_authors))
# count = 0
# unique_authors_dict = {}
# for auth in unique_authors_list:
#     unique_authors_dict[auth] = count
#     count +=1



# # construct dict for echarts
# big_dict = {'nodes':[], 'links':[]}
# for k,v in unique_authors_dict.items():
#     big_dict['nodes'].append({'id': v, 
#                             'name': k,
#                             'draggable': True})
#                             # 'category': cat(k)})
# # format to suit echarts
# for i in range(len(influencer_df)):
#     for k in influencer_df['related_25'][i]:
#         big_dict['links'].append( {'source': unique_authors_dict[influencer_df['username'][i]],
#                                 'target': unique_authors_dict[k],
#                                 'lineStyle': {'color':'#D3D3D3'},
#                                 'label': {'show': True, 'formatter':'{c}'}
#                                 })

# with open('data/inf_graph.json', 'w') as fp:
#     json.dump(big_dict, fp)
def broad_cat(x):
    if type(x)==float:
        return 'Other'
    return list(CATEGORY_DICT.keys())[[x in y for y in CATEGORY_DICT.values()].index(True)]
influencer_df['broad_category'] = influencer_df['category_name'].apply(lambda x: broad_cat(x))
for i,j in enumerate(influencer_df['related_influencers']):
    influencer_df['related_influencers'][i] = ast.literal_eval(j)
influencer_df = influencer_df.drop_duplicates(subset=['name','biography'],keep='last').reset_index(drop=True)
# drop rows with no related influencers
influencer_df['len_related'] = influencer_df['related_influencers'].apply(lambda x: len(x))
drop_index = influencer_df.loc[influencer_df['len_related']==0].index
influencer_df = influencer_df.drop(index=drop_index).reset_index(drop=True)

# take top 10 related influencers
influencer_df['related_25'] = influencer_df['related_influencers'].apply(lambda x: x[:10])

# give each author a unique id
all_authors = list(influencer_df['username'])
for i in influencer_df['related_25']:
    all_authors.extend(i)
unique_authors_list = list(set(all_authors))
count = 0
unique_authors_dict = {}
for auth in unique_authors_list:
    unique_authors_dict[auth] = count
    count +=1

def cat(username):
    try:
        cate = influencer_df.loc[influencer_df['username']==username]['broad_category'].values[0]
    except:
        cate = 'External Related Influencer'
    if cate == 'Fashion':
        return 0
    elif cate == 'Health/Wellness':
        return 1
    elif cate == 'Media':
        return 2
    elif cate == 'Food':
        return 3
    elif cate == 'Electronics':
        return 4
    elif cate == 'Education':
        return 5
    elif cate == 'Other':
        return 6
    elif cate == 'Business':
        return 7
    elif cate == 'For Good':
        return 8
    elif cate == 'External Related Influencer':
        return 9

# construct dict for echarts
big_dict = {'nodes':[], 'links':[], 'categories':[{'name': "Fashion"}, {'name': "Health/Wellness"}, {'name': "Media"},{'name': "Food"},{'name': "Electronics"},{'name': "Education"},{'name': "Other"},{'name': "Business"},{'name': "For Good"},{'name': "External Related Influencer"}]}
for k,v in unique_authors_dict.items():
    big_dict['nodes'].append({'id': v, 
                            'name': k,
                            'draggable': True,
                            'category': cat(k)})
# format to suit echarts
for i in range(len(influencer_df)):
    for k in influencer_df['related_25'][i]:
        big_dict['links'].append( {'source': unique_authors_dict[influencer_df['username'][i]],
                                'target': unique_authors_dict[k],
                                'lineStyle': {'color':'#D3D3D3'},
#                                 'label': {'show': True, 'formatter':'{c}'}
                                })

with open('data/inf_graph_colour.json', 'w') as fp:
    json.dump(big_dict, fp)

with open('data/unique_authors_dict_saved.json', 'w') as fp:
    json.dump(unique_authors_dict, fp)