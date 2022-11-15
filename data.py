import pandas as pd 
import numpy as np

data = pd.read_csv('data/influencers_with-profile-pic.csv')

def get_card_data(index): 
    name = data['name'][index]
    username = "@" + data['username'][index] 
    biography = data['biography'][index]
    num_followers = int(data['num_followers'][index])
    dp_path = '/assets/images/' + username[1:] + '.jpg'

    return name, username, biography, num_followers, dp_path