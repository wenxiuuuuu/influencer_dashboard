import pandas as pd 
import numpy as np
import json

### change the influencers by changing the csv file inserted here. after every analysis can save as a new csv file then insert here!!!! 

data = pd.read_csv('data/influencers_with-profile-pic.csv')
# influencer_posts_df = pd.read_csv('data/influencer_post_db_temp.csv')

def get_card_data(index): 
    name = data['name'][index]
    username = "@" + data['username'][index] 
    biography = data['biography'][index]
    num_followers = int(data['num_followers'][index])
    dp_path = '/assets/images/' + username[1:] + '.jpg'

    return name, username, biography, num_followers, dp_path

def get_profile_data(index): 

    # basic data 
    name = data['name'][index]
    username = "@" + data['username'][index] 
    biography = data['biography'][index]
    num_followers = int(data['num_followers'][index])
    dp_path = '/assets/images/' + username[1:] + '.jpg'   

    recent_post = data['recent_pic_short'][index] # recent post url 

    # more data to get 
    # avg_engagement = data['avg_engagement'][index] ## NEED TO CALCULATE 
    # brands_worked_with = data['brands_worked_with'][index] ## IN A LIST? 
    # hashtags = data['hashtags'][index] ## IN A LIST

 
    # # 1. for pie chart (type of posts) ## THIS IS FAKE DATA
    # labels = ['Images', 'Sidecars', 'Videos']
    # values = [17, 13, 20]

    # res = dict(zip(labels, values))
    # data_pie = json.dumps(res)

    data_pie = [
        { 'value': 17, 'name': 'Images' },
        { 'value': 13, 'name': 'Sidecars' },
        { 'value': 20, 'name': 'Videos' },
    ]
    # # 2. radio chart 

    # # 3. pie chart (num sponsored?)

    # # network graphs (cammy done)



    return name, username, biography, num_followers, dp_path, recent_post, data_pie


def radial_data(index):
    name, username, biography, num_followers, dp_path = get_card_data(index)
    username = username[1:]
    print("!!!!!!!", username)
    influencer_posts_df = pd.read_csv('data/influencer_posts_df_1.csv')
    # influencer_profile_df = pd.read_csv('../influencers_with-profile-pic.csv')
    # influencer_posts_df = pd.read_csv('../influencer_posts_df_1.csv')
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

    # average
    influencer_profile_df['num_followers'] = influencer_profile_df['num_followers'].fillna(0)
    influencer_posts_df['edge_media_to_comment'] = influencer_posts_df['edge_media_to_comment'].fillna(0)
    influencer_posts_df['edge_liked_by'] = influencer_posts_df['edge_liked_by'].fillna(0)
    influencer_posts_df['video_view_count'] = influencer_posts_df['video_view_count'].fillna(0)
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
    print('helllo',len(bin_df))
    # current
    influencer_likes = bin_df.loc[bin_df['username']==username,'likes'].values[0]
    influencer_comments = bin_df.loc[bin_df['username']==username,'comments'].values[0]
    influencer_followers = bin_df.loc[bin_df['username']==username,'followers'].values[0]
    influencer_video_views = bin_df.loc[bin_df['username']==username,'video_views'].values[0]

    return username, total_avg_likes, total_avg_comments, total_avg_followers, total_avg_video_views, influencer_likes, influencer_comments, influencer_followers, influencer_video_views

def dropdown_options():
    options = []
    for i in range(len(data)): 
        dic_item = {"label": [], "value": []}
        dic_item["label"] = data['username'][i]
        dic_item["value"] = i
        options.append(dic_item)
    return options 
