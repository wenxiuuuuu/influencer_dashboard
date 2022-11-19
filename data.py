import pandas as pd 
pd.options.mode.chained_assignment = None
import numpy as np
import json
import re
import pickle
from collections import Counter
from mongodata import influencer_df, post_df, category_dict, get_cur_infl_profile
from constants import * 
import ast

### change the influencers by changing the csv file inserted here. after every analysis can save as a new csv file then insert here!!!! 

# pickle file contains each influencer or brand with his/her/its category
# {'annettelee': 'Artist', 'uniqlosg': 'Clothing store'}
# with open('data/profile_category_dict.pkl', 'rb') as f:
#     company_cat = pickle.'/assets/images/' + username[1:] + '.jpg'   load(f)

# data = pd.read_csv('data/influencers_with-profile-pic.csv')
# influencer_posts_df = pd.read_csv('data/influencer_post_db_temp.csv')
# influencer_posts_df = pd.read_csv('data/influencer_posts_df_1.csv')
# data = pd.read_csv('data/influencer_db_17112022.csv')
# influencer_posts_df = pd.read_csv('data/influencer_posts_df_1.csv')
# influencer_stats = pd.read_csv('data/influencer_stats.csv')
# data = influencer_df
# influencer_posts_df = post_df

def pie_data(username):
    current_influencer_profile = get_cur_infl_profile(username)

    # pie_data = [
    #     {'value': current_influencer_profile['GraphSidecar'].values[0], 'name': 'Sliding Imgaes'},
    #     {'value': current_influencer_profile['GraphVideo'].values[0], 'name': 'Video'},
    #     {'value': current_influencer_profile['GraphImage'].values[0], 'name': 'Single Image'}
    # ]
    pie_data = []
    if current_influencer_profile['GraphSidecar'].values[0] != 0:
        pie_data.append({'value': current_influencer_profile['GraphSidecar'].values[0], 'name': 'Sliding Images'})
    if current_influencer_profile['GraphVideo'].values[0] != 0:
        pie_data.append({'value': current_influencer_profile['GraphVideo'].values[0], 'name': 'Video'})
    if current_influencer_profile['GraphImage'].values[0] != 0:
        pie_data.append({'value': current_influencer_profile['GraphImage'].values[0], 'name': 'Single Image'})

    # for k,v in post_type.items():
    #     pie_data.append( {'value': v, 'name': k} )
    return pie_data

# create bins for radial graph
bin_dict = {}
labels = [1,2,3,4,5]
bin_dict['likes'] = pd.qcut(post_df.groupby('username')['edge_liked_by'].mean(), len(labels), labels=labels).values
bin_dict['comments'] = pd.qcut(post_df.groupby('username')['edge_media_to_comment'].mean(), len(labels), labels=labels).values
bin_dict['video_views'] = pd.qcut(post_df.groupby('username')['video_view_count'].mean(), len(labels), labels=labels).values
bin_dict['followers'] = pd.qcut(influencer_df['num_followers'], len(labels), labels=labels).values
bin_df = pd.DataFrame(bin_dict).astype(int)

# average benchmark
total_avg_likes = bin_df['likes'].mean()
total_avg_comments = bin_df['comments'].mean()
total_avg_followers = bin_df['followers'].mean()
total_avg_video_views = bin_df['video_views'].mean()

bin_df['username'] = influencer_df.sort_values('username')['username'].values


def radial_data(username):
    # current
    influencer_likes = bin_df.loc[bin_df['username']==username,'likes'].values[0]
    influencer_comments = bin_df.loc[bin_df['username']==username,'comments'].values[0]
    influencer_followers = bin_df.loc[bin_df['username']==username,'followers'].values[0]
    influencer_video_views = bin_df.loc[bin_df['username']==username,'video_views'].values[0]

    return username, total_avg_likes, total_avg_comments, total_avg_followers, total_avg_video_views, influencer_likes, influencer_comments, influencer_followers, influencer_video_views


## utilities 
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
    current_influencer_posts = post_df[post_df['username'] == username]
    # current_influencer_posts = current_influencer_posts.apply(parse_caption, axis=1)

    result_dict = {}
    # result_dict['avg_comments'] = current_influencer_posts['edge_media_to_comment'].mean()
    # result_dict['avg_likes'] = current_influencer_posts['edge_liked_by'].mean()
    # result_dict['post_type'] = dict(current_influencer_posts['post_type'].value_counts())
    # result_dict['avg_video_views'] = current_influencer_posts['video_view_count'].mean()
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
    
    mentions_category = [category_dict.get(i) for i in all_mentions if category_dict.get(i)]
    category_counts = Counter(mentions_category)
    # print(category_counts)
    result_dict['category_counts'] = category_counts
    
    all_mentions_cats = [(i, category_dict.get(i))for i in all_mentions if category_dict.get(i)]
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


def dropdown_options():
    options = []
    for i in range(len(influencer_df)): 
        dic_item = {"label": [], "value": []}
        dic_item["label"] = influencer_df['username'][i]
        dic_item["value"] = influencer_df['username'][i]
        options.append(dic_item)
    return options 


def get_filtered_influ_df(ig_text, follower_range, cate):
    finegrained_cate = CATEGORY_DICT.get(cate, [])
    # TODO: check if in our db
    filtered_df = influencer_df[(influencer_df['num_followers']>=follower_range[0]) & (influencer_df['num_followers']<=follower_range[1])]
    filtered_df = filtered_df[filtered_df['top_category'].isin(finegrained_cate)]
    return filtered_df

def get_categ_count(row, category):
    finegrained_cate = CATEGORY_DICT.get(category, [])
    cur_categs = row['category_count']
    keys  = [cur_categs.keys]
    common = list(set(keys).intersection(set(finegrained_cate)))
    print('common', common)
    count = 0 
    for c in common:
        count += cur_categs[c]
    try:
        count = cur_categs['Clothing (Brand)']
    except:
        count = 0
    return count

def get_categ_count_df(category, filtered_df):
    cat_dicts = list(filtered_df['category_count'])
    finegrained_cate = category_dict.get(category, [])
    counts = []
    for c in cat_dicts:                                                     
        c =  ast.literal_eval(c)
        count = 0
        for cat in list(c.keys()):
            # print(cat)
            if cat in finegrained_cate:
                count += c[cat]
        counts.append(count)    
    filtered_df['cat_count'] = counts
    return filtered_df

def rank_filtered_df(filtered_df, category):
    # influencer_stats
    filtered_df['follower_ranking'] = filtered_df['num_followers'].rank(pct=True)
    filtered_df['likes_ranking'] = filtered_df['avg_likes'].rank(pct=True)
    filtered_df['comments_ranking'] = filtered_df['avg_comments'].rank(pct=True)
    filtered_df['views_ranking'] = filtered_df['avg_video_views'].rank(pct=True)
    filtered_df = get_categ_count_df(category, filtered_df)
    filtered_df['total_ranking'] = filtered_df['follower_ranking'] + filtered_df['likes_ranking'] + filtered_df['comments_ranking'] + filtered_df['views_ranking'] + filtered_df['cat_count']
    filtered_df = filtered_df.sort_values('total_ranking', ascending = False)
    return filtered_df


if __name__ == '__main__':
    print(get_influencer_statistics('parisabong'))