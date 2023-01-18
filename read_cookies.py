import pickle

with open('parser/my_cookies.dat', 'rb') as f:
    print(pickle.load(f))
