import re
import sys
import requests
import json
from contextlib import closing


def request_imdb(imdb_id):
    url = 'http://www.omdbapi.com/?i={}&plot=short&r=json'.format(imdb_id)
    r = requests.get(url)
    return r.json()


def top_250_ids():
    with closing(open('top250.txt')) as f:
        return [(i+1, line.rstrip('\r\n')) for i, line in enumerate(f)]


def fetch_remote():
    ids = top_250_ids()
    movies = [(i, request_imdb(id)) for i, id in ids]
    return movies


def save_to_cache(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


def fetch_local():
    with open('data.json', 'r') as f:
        data = json.load(f)
        return data


def fetch_movies():
    try:
        data = fetch_local()
    except IOError as e:
        print("fetching data from remote api...")
        data = fetch_remote()
        save_to_cache(data)
    return data
