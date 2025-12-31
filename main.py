import requests
import json
import os
import time
from datetime import datetime, timedelta

BASE_URL = 'https://ll.thespacedevs.com/2.0.0/launch/'
API_KEY = '9b91363961799d7f79aabe547ed0f7be914664dd'
CACHE_FILE = 'cache.json'
CACHE_DURATION_HOURS = 24  # Refresh cache if older than this

def fetch_launches(url, params):
    launches = []
    headers = {'Authorization': f'Token {API_KEY}'}
    while url:
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            launches.extend(data['results'])
            url = data.get('next')
            params = None  # params only for first request
            if url:
                time.sleep(2)  # Delay to respect rate limits
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("Rate limit exceeded, sleeping 60 seconds...")
                time.sleep(60)
                continue
            else:
                raise
    return launches

def get_upcoming_launches():
    today = datetime.now().date()
    url = BASE_URL + 'upcoming/'
    params = {
        'net__gte': today.isoformat(),
        'net__lte': (today + timedelta(days=30)).isoformat(),
        'limit': 50
    }
    return fetch_launches(url, params)

def get_past_launches():
    today = datetime.now().date()
    url = BASE_URL + 'previous/'
    params = {
        'net__gte': (today - timedelta(days=30)).isoformat(),
        'limit': 50
    }
    return fetch_launches(url, params)

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)
            last_updated = datetime.fromisoformat(data['last_updated'])
            if datetime.now() - last_updated < timedelta(hours=CACHE_DURATION_HOURS):
                return data['launches']
    return None

def save_cache(launches):
    data = {
        'last_updated': datetime.now().isoformat(),
        'launches': launches
    }
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_all_launches():
    cached = load_cache()
    if cached:
        print("Using cached data.")
        return cached
    print("Fetching data from API...")
    upcoming = get_upcoming_launches()
    past = get_past_launches()
    all_launches = {'upcoming': upcoming, 'past': past}
    save_cache(all_launches)
    return all_launches

if __name__ == '__main__':
    launches = get_all_launches()
    print(f"Upcoming launches: {len(launches['upcoming'])}")
    print(f"Past launches: {len(launches['past'])}")