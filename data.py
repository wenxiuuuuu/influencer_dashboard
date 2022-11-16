import pandas as pd 
import numpy as np


### change the influencers by changing the csv file inserted here. after every analysis can save as a new csv file then insert here!!!! 

data = pd.read_csv('data/influencers_with-profile-pic.csv')

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
    # labels = ['image', 'sidecar', 'video']
    # values = [17, 13, 20]

    # # 2. radio chart 

    # # 3. pie chart (num sponsored?)

    # # network graphs (cammy done)



    return name, username, biography, num_followers, dp_path, recent_post

# def generate_pie_chart(label, values): 
