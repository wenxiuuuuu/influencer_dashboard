import numpy as np
import pickle
from urllib.request import urlopen


# url = 'https://drive.google.com/uc?export=view&id=1Yqdz86fVk5krNXs7hju6g5RkSPS_BUll'

url = 'https://drive.google.com/u/0/uc?id=1Yqdz86fVk5krNXs7hju6g5RkSPS_BUll&export=download&confirm=t&uuid=59d57eb8-9bbf-4343-a92c-e970f15839fe&at=AHV7M3e9-gyET6zhVR8uQJfdd-mT:1669367383905'
loaded_pickle_object = pickle.load(urlopen(url))

