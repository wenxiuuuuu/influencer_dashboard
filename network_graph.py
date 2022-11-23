import ast
import json

from mongodata import influencer_df

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



# construct dict for echarts
big_dict = {'nodes':[], 'links':[]}
for k,v in unique_authors_dict.items():
    big_dict['nodes'].append({'id': v, 
                            'name': k,
                            'draggable': True})
                            # 'category': cat(k)})
# format to suit echarts
for i in range(len(influencer_df)):
    for k in influencer_df['related_25'][i]:
        big_dict['links'].append( {'source': unique_authors_dict[influencer_df['username'][i]],
                                'target': unique_authors_dict[k],
                                'lineStyle': {'color':'#D3D3D3'},
                                'label': {'show': True, 'formatter':'{c}'}
                                })

with open('data/inf_graph.json', 'w') as fp:
    json.dump(big_dict, fp)