from instaloader import Profile
import instaloader
import pymongo
import time
from datetime import datetime

def get_instaloader():
    L = instaloader.Instaloader()
    L.load_session_from_file('tehbing1234')
    return L

def get_user_posts(profile, latest_post_time):
    user_posts = []
    for idx, post in enumerate(profile.get_posts()):
        # print('idx', idx)
        if post.date_utc.timestamp() < latest_post_time:
            print('posts are all updated')
            return user_posts
        print('post time', post.date_utc.timestamp(), post.date_utc)
        post_details  = {}
        post_details['username'] = profile.username
        post_details['post_type'] = post.typename
        post_details['display_url'] = post.url
        post_details['is_video'] = post.is_video
        post_details['edge_media_to_caption'] = post.caption
        post_details['edge_media_to_comment'] = post.comments
        post_details['taken_at_timestamp'] = post.date_utc.timestamp()
        post_details['edge_liked_by'] = post.likes
        post_details['edge_media_to_tagged_users'] = post.tagged_users
        post_details['shortcode'] = post.shortcode


        if post_details['is_video']:
            post_details['video_view_count'] = post.video_view_count
            post_details['video_duration'] = post.video_duration
        else:
            post_details['video_view_count'] = -1
            post_details['video_duration'] = -1


        # extra stuff that instaloader has
        post_details['caption_hashtags'] = post.caption_hashtags

        user_posts.append(post_details)

        time.sleep(10)

    return user_posts



if __name__ == "__main__":
    conn_str = 'mongodb+srv://keiwuai30off:CZ4125keiwuaiupgrade@cluster0.aqgyhxf.mongodb.net/?retryWrites=true&w=majority'
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    db1 = client['influencer_db']
    cursor = db1.posts
    all_usernames = cursor.distinct('username')
    print('total number to update: ', len(all_usernames))
    # all_usernames = ['huinileee']

    instaloader_client = get_instaloader()

    for username in all_usernames:
        print(f'updating {username}...')
        latest_post_time = max([i['taken_at_timestamp'] for i in cursor.find({'username': username})])
        print('currently most updated until: ', datetime.fromtimestamp(latest_post_time))
        profile = Profile.from_username(instaloader_client.context, username)
        new_posts = get_user_posts(profile, latest_post_time)
        print(new_posts)
        if new_posts:
            print(f'inserting {len(new_posts)} documents...')
            cursor.insert_many(new_posts)


