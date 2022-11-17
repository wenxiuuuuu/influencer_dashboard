import pymongo
import pandas as pd

conn_str = "mongodb+srv://keiwuai30off:CZ4125keiwuaiupgrade@cluster0.aqgyhxf.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
print(client.server_info()) # just a sanity check

db1 = client['influencer_db']
influencers = db1.profile_info
posts = db1.posts

doc_list = []
for document in posts.find():
    doc_list.append(document)
post_df = pd.DataFrame(doc_list)

doc_list = []
for document in influencers.find():
    doc_list.append(document)
influencer_df = pd.DataFrame(doc_list)

def get_cur_infl_profile(username):
    return influencer_df[influencer_df['username']==username]

def get_influencer_category_counts(username):
    return get_cur_infl_profile(username)['category_count'].iloc[0]

def get_influencer_top_category(username):
    return get_cur_infl_profile(username)['top_category'].iloc[0]

