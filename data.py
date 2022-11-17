import pandas as pd 
import numpy as np
import json
import re
import pickle
from collections import Counter

### change the influencers by changing the csv file inserted here. after every analysis can save as a new csv file then insert here!!!! 

# pickle file contains each influencer or brand with his/her/its category
# {'annettelee': 'Artist', 'uniqlosg': 'Clothing store'}
with open('data/profile_category_dict.pkl', 'rb') as f:
    company_cat = pickle.load(f)

# data = pd.read_csv('data/influencers_with-profile-pic.csv')
# influencer_posts_df = pd.read_csv('data/influencer_post_db_temp.csv')
# influencer_posts_df = pd.read_csv('data/influencer_posts_df_1.csv')
data = pd.read_csv('data/influencer_db_17112022.csv')
influencer_posts_df = pd.read_csv('data/influencer_posts_df_1.csv')
influencer_posts_df['edge_media_to_caption'] = influencer_posts_df['edge_media_to_caption'].replace(np.nan, '')


# get intersection of both df
profile_user = list(data['username'])
post_user = list(influencer_posts_df['username'])
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
intersect_list = intersection(profile_user, post_user)
influencer_profile_df = data[data['username'].isin(intersect_list)]
influencer_posts_df = influencer_posts_df[influencer_posts_df['username'].isin(intersect_list)]

influencer_profile_df['num_followers'] = influencer_profile_df['num_followers'].fillna(0)
influencer_posts_df['edge_media_to_comment'] = influencer_posts_df['edge_media_to_comment'].fillna(0)
influencer_posts_df['edge_liked_by'] = influencer_posts_df['edge_liked_by'].fillna(0)
influencer_posts_df['video_view_count'] = influencer_posts_df['video_view_count'].fillna(0)


# def get_card_data(index): 
#     name = data['name'][index]
#     username = "@" + data['username'][index] 
#     biography = data['biography'][index]
#     num_followers = int(data['num_followers'][index])
#     dp_path = '/assets/images/' + username[1:] + '.jpg'

#     return name, username, biography, num_followers, dp_path


# function to extract hashtags and mentions from captions
# def parse_caption(row):
#     mentions = [re.sub('[^0-9a-zA-Z_\.]+', '', i[1:]) for i in row.edge_media_to_caption.split() if i.startswith('@')]
#     hashtags = [i[1:] for i in row.edge_media_to_caption.split() if i.startswith('#')]
#     all_mentions = set(mentions + eval(row['edge_media_to_tagged_users']))
#     all_mentions = list(all_mentions)
#     row['mentions'] = all_mentions
#     row['hashtags'] = hashtags
#     return row

# def get_influencer_statistics(df):
#     """_summary_
#     Args:
#         df (pd.DataFrame): current_influencer_posts
#         num_followers (int): number of followers for this influencer

#     Returns:
#         Dict: Useful information to display
#             avg_comments: float
#             avg_likes: float
#             post_type: dict[type: count] GraphVideo GraphSidecar GraphImage
#             avg_video_views: float
#             mentions: top 10 mentions
#             hashtags: top 10 hashtags
#     """
#     result_dict = {}
#     # result_dict['num_followers'] = num_followers
#     result_dict['avg_comments'] = df['edge_media_to_comment'].mean()
#     result_dict['avg_likes'] = df['edge_liked_by'].mean()
#     result_dict['post_type'] = dict(df['post_type'].value_counts())
#     result_dict['avg_video_views'] = df['video_view_count'].mean()
#     all_mentions = []
#     for row in df['mentions']:
#         for i in row:
#             all_mentions.append(i)
#     mention_counts = sorted(Counter(all_mentions).items(), key=lambda item: -item[1])

#     top_mentions = [i[0] for i in mention_counts][:10]
#     result_dict['mentions'] = top_mentions
    
#     all_hashtags = []
#     for row in df['hashtags']:
#         for i in row:
#             all_hashtags.append(i.lower())
#     hashtag_counts = sorted(Counter(all_hashtags).items(), key=lambda item: -item[1])

#     top_hashtags = [i[0] for i in hashtag_counts][:10]
#     result_dict['hashtags'] = top_hashtags
    
#     mentions_category = [company_cat.get(i) for i in all_mentions if company_cat.get(i)]
#     category_counts = Counter(mentions_category)
#     # print(category_counts)
#     result_dict['category_counts'] = category_counts
    
#     return result_dict

data = influencer_profile_df.sort_values('username').reset_index(drop=True)

def get_data_length(): 
    return len(data)

def get_profile_data(index): 

    # basic data 
    name = data['name'][index]
    username = "@" + data['username'][index] 
    biography = data['biography'][index]
    num_followers = int(data['num_followers'][index])
    dp_path = '/assets/images/' + username[1:] + '.jpg'   
    recent_post = data['recent_pic_short'][index] # recent post url 

    # current_influencer_posts = influencer_posts_df[influencer_posts_df['username'] == username[1:]]
    # current_influencer_posts = current_influencer_posts.apply(parse_caption, axis=1)
    influencer_stats_dict = get_influencer_statistics(username[1:])
    avg_comments = int(influencer_stats_dict['avg_comments'])
    avg_likes = int(influencer_stats_dict['avg_likes'])
    avg_video_views = int(influencer_stats_dict['avg_video_views'])
    post_type = influencer_stats_dict['post_type']
    mentions = influencer_stats_dict['mentions']
    hashtags = influencer_stats_dict['hashtags']
    category_counts = influencer_stats_dict['category_counts']

    return name, username, biography, num_followers, dp_path, recent_post, avg_comments, avg_likes, avg_video_views, post_type, mentions, hashtags, category_counts

def pie_data(index):
    _, _, _, _, _, _, _, _, _, post_type, _, _, _ = get_profile_data(index)

    pie_data = []
    for k,v in post_type.items():
        pie_data.append( {'value': v, 'name': k} )

    # pie_data = [
    #     { 'value': 17, 'name': 'Images' },
    #     { 'value': 13, 'name': 'Sidecars' },
    #     { 'value': 20, 'name': 'Videos' },
    # ]
    return pie_data

def radial_data(index):
    name, username, biography, num_followers, dp_path, recent_post, avg_comments, avg_likes, avg_video_views, post_type, mentions, hashtags, category_counts = get_profile_data(index)
    # _, username, _, _, _ = get_card_data(index)
    username = username[1:]
    # influencer_posts_df = pd.read_csv('data/influencer_posts_df_1.csv')
    # influencer_posts_df['edge_media_to_caption'] = influencer_posts_df['edge_media_to_caption'].replace(np.nan, '')

    # # get intersection of both df
    # profile_user = list(data['username'])
    # post_user = list(influencer_posts_df['username'])
    # def intersection(lst1, lst2):
    #     lst3 = [value for value in lst1 if value in lst2]
    #     return lst3
    # intersect_list = intersection(profile_user, post_user)
    # influencer_profile_df = data[data['username'].isin(intersect_list)]
    # influencer_posts_df = influencer_posts_df[influencer_posts_df['username'].isin(intersect_list)]

    # # average
    # influencer_profile_df['num_followers'] = influencer_profile_df['num_followers'].fillna(0)
    # influencer_posts_df['edge_media_to_comment'] = influencer_posts_df['edge_media_to_comment'].fillna(0)
    # influencer_posts_df['edge_liked_by'] = influencer_posts_df['edge_liked_by'].fillna(0)
    # influencer_posts_df['video_view_count'] = influencer_posts_df['video_view_count'].fillna(0)
    bin_dict = {}
    labels = [1,2,3,4,5]
    bin_dict['likes'] = pd.qcut(influencer_posts_df.groupby('username')['edge_liked_by'].mean(), len(labels), labels=labels).values
    bin_dict['comments'] = pd.qcut(influencer_posts_df.groupby('username')['edge_media_to_comment'].mean(), len(labels), labels=labels).values
    bin_dict['video_views'] = pd.qcut(influencer_posts_df.groupby('username')['video_view_count'].mean(), len(labels), labels=labels).values
    bin_dict['followers'] = pd.qcut(influencer_profile_df['num_followers'], len(labels), labels=labels).values
    bin_df = pd.DataFrame(bin_dict).astype(int)

    # average benchmark
    total_avg_likes = bin_df['likes'].mean()
    total_avg_comments = bin_df['comments'].mean()
    total_avg_followers = bin_df['followers'].mean()
    total_avg_video_views = bin_df['video_views'].mean()

    bin_df['username'] = influencer_profile_df.sort_values('username')['username'].values
    # current
    influencer_likes = bin_df.loc[bin_df['username']==username,'likes'].values[0]
    influencer_comments = bin_df.loc[bin_df['username']==username,'comments'].values[0]
    influencer_followers = bin_df.loc[bin_df['username']==username,'followers'].values[0]
    influencer_video_views = bin_df.loc[bin_df['username']==username,'video_views'].values[0]

    return username, total_avg_likes, total_avg_comments, total_avg_followers, total_avg_video_views, influencer_likes, influencer_comments, influencer_followers, influencer_video_views


## utilities 

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

def get_influencer_statistics(username):
    """_summary_

    Args:
        df (pd.DataFrame): Profile dataframe

    Returns:
        Dict: Useful information to display
            avg_comments: float
            avg_likes: float
            post_type: dict[type: count] GraphVideo GraphSidecar GraphImage
            avg_video_views: float
            mentions: top 10 mentions
            hashtags: top 10 hashtags
            
    """
    current_influencer_posts = influencer_posts_df[influencer_posts_df['username'] == username]
    current_influencer_posts = current_influencer_posts.apply(parse_caption, axis=1)

    result_dict = {}
    result_dict['avg_comments'] = current_influencer_posts['edge_media_to_comment'].mean()
    result_dict['avg_likes'] = current_influencer_posts['edge_liked_by'].mean()
    result_dict['post_type'] = dict(current_influencer_posts['post_type'].value_counts())
    result_dict['avg_video_views'] = current_influencer_posts['video_view_count'].mean()
    all_mentions = []
    # print(len(current_influencer_posts['mentions']))
    for row in current_influencer_posts['mentions']:
        # for i in eval(row):
        for i in row:
            all_mentions.append(i)
    mention_counts = sorted(Counter(all_mentions).items(), key=lambda item: -item[1])
    # print(mention_counts)  # debug
    top_mentions = [i[0] for i in mention_counts][:10]
    result_dict['mentions'] = top_mentions
    
    all_hashtags = []
    for row in current_influencer_posts['hashtags']:
        # for i in eval(row):
        for i in row:
            all_hashtags.append(i.lower())
    hashtag_counts = sorted(Counter(all_hashtags).items(), key=lambda item: -item[1])
    # print(hashtag_counts)  # debug
    top_hashtags = [i[0] for i in hashtag_counts][:10]
    result_dict['hashtags'] = top_hashtags
    
    mentions_category = [company_cat.get(i) for i in all_mentions if company_cat.get(i)]
    category_counts = Counter(mentions_category)
    # print(category_counts)
    result_dict['category_counts'] = category_counts
    
    all_mentions_cats = [(i, company_cat.get(i))for i in all_mentions if company_cat.get(i)]
    # print(all_mentions_cats)
    if all_mentions_cats:
        user, cat = zip(*all_mentions_cats)
        result_dict['username_cat_df'] = pd.DataFrame({
            'username': user,
            'category': cat 
        })
    else:
        result_dict['username_cat_df'] = pd.DataFrame({
            'username': [],
            'category': [] 
        })
    
    return result_dict

# print(get_influencer_statistics('parisabong').keys())

def dropdown_options():
    options = []
    for i in range(len(data)): 
        dic_item = {"label": [], "value": []}
        dic_item["label"] = data['username'][i]
        dic_item["value"] = i
        options.append(dic_item)
    return options 

