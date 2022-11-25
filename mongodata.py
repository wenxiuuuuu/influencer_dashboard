import pymongo
import numpy as np
import re
import pandas as pd
pd.options.mode.chained_assignment = None

conn_str = "mongodb+srv://keiwuai30off:CZ4125keiwuaiupgrade@cluster0.aqgyhxf.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
print(client.server_info()) # just a sanity check

db1 = client['influencer_db']
influencers = db1.profile_info
posts = db1.posts
category = db1.category

# post_df
doc_list = []
for document in posts.find():
    doc_list.append(document)
post_df = pd.DataFrame(doc_list)

# influencer_df
doc_list = []
for document in influencers.find():
    doc_list.append(document)
influencer_df = pd.DataFrame(doc_list)

# 1. final category_dict
category_dict = {}
for document in category.find():
    category_dict[document['username']] = document['category']

post_df['edge_media_to_caption'] = post_df['edge_media_to_caption'].replace(np.nan, '')


# get intersection of influencer_df and post_df
profile_user = list(influencer_df['username'])
post_user = list(post_df['username'])
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
intersect_list = intersection(profile_user, post_user)
influencer_df = influencer_df[influencer_df['username'].isin(intersect_list)]
post_df = post_df[post_df['username'].isin(intersect_list)]

influencer_df['num_followers'] = influencer_df['num_followers'].fillna(0)
post_df['edge_media_to_comment'] = post_df['edge_media_to_comment'].fillna(0)
post_df['edge_liked_by'] = post_df['edge_liked_by'].fillna(0)
post_df['video_view_count'] = post_df['video_view_count'].fillna(0)

# 2. final influencer_df
influencer_df = influencer_df.sort_values('username').reset_index(drop=True)
pattern = re.compile('[\W_]+')
influencer_df['username_html'] = influencer_df['username'].apply(lambda x: pattern.sub('', x))


def parse_caption(row):
    # print(row.edge_media_to_caption)
    mentions = [re.sub('[^0-9a-zA-Z_\.]+', '', i[1:]) for i in row.edge_media_to_caption.split() if i.startswith('@')]
    hashtags = [i[1:] for i in row.edge_media_to_caption.split() if i.startswith('#')]
    all_mentions = set(mentions + eval(row['edge_media_to_tagged_users']))
    all_mentions = list(all_mentions)
    # print('all mentions', all_mentions)
    row['mentions'] = all_mentions
    row['hashtags'] = hashtags
    return row


# 3. final post_df
post_df = post_df.apply(parse_caption, axis=1)

def get_cur_infl_profile(username):
    return influencer_df[influencer_df['username']==username]

def get_influencer_category_counts(username):
    return get_cur_infl_profile(username)['category_count'].iloc[0]

def get_influencer_top_category(username):
    return get_cur_infl_profile(username)['top_category'].iloc[0]

# 4. final comments_df
comments_df = pd.read_csv('data/influencer_comments_sentiments.csv')
# get the influencer username
comments_user = comments_df['username'].unique()
idx = comments_df.groupby(['username','binary_class'])['binary_score'].transform(max) == comments_df['binary_score']
## get most neg&pos comment for each influencer
subset_df = comments_df[idx].reset_index(drop=True).drop_duplicates(subset=['comments'], keep='first').drop(index=15).reset_index(drop=True)



if __name__ == '__main__':
    print('helo')
    # print(influencer_df.loc[influencer_df['username']=='ianjeevan_']['username_html'].values[0])
    # print(list(post_df.columns))
    # print()
    # print(list(influencer_df['top_category'].unique()))
    uniquelist = []
    for v in category_dict.values():
        uniquelist.append(v)
    print(set(uniquelist))
    print()
    influencer_df.to_csv('influencer_df.csv', index=False)