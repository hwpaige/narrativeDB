import requests
import json
import os
import pandas as pd
from datetime import datetime, timedelta
from models import Launch, SessionLocal, init_db

BASE_URL = 'https://fdo.rocketlaunch.live/json/launches/'

def get_upcoming_launches():
    params = {'key': '9b91363961799d7f79aabe547ed0f7be914664dd'}
    response = requests.get(BASE_URL + 'next/5', params=params)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list):
        return pd.DataFrame(data)
    else:
        return pd.DataFrame(data.get('result', []))

def get_past_launches():
    params = {'key': '9b91363961799d7f79aabe547ed0f7be914664dd'}
    response = requests.get(BASE_URL + 'past/5', params=params)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list):
        return pd.DataFrame(data)
    else:
        return pd.DataFrame(data.get('result', []))

def save_to_db(df, launch_type):
    session = SessionLocal()
    for _, row in df.iterrows():
        launch_data = {
            'id': row['id'],
            'cospar_id': row.get('cospar_id'),
            'sort_date': row.get('sort_date'),
            'name': row.get('name'),
            'provider': json.dumps(row.get('provider')) if row.get('provider') else None,
            'vehicle': json.dumps(row.get('vehicle')) if row.get('vehicle') else None,
            'pad': json.dumps(row.get('pad')) if row.get('pad') else None,
            'location': json.dumps(row.get('location')) if row.get('location') else None,
            'agencies': json.dumps(row.get('agencies')) if row.get('agencies') else None,
            'mission': json.dumps(row.get('mission')) if row.get('mission') else None,
            'mission_type': row.get('mission_type'),
            'orbit': json.dumps(row.get('orbit')) if row.get('orbit') else None,
            'launch_description': row.get('launch_description'),
            'win_open': pd.to_datetime(row.get('win_open')) if row.get('win_open') else None,
            't0': pd.to_datetime(row.get('t0')) if row.get('t0') else None,
            'win_close': pd.to_datetime(row.get('win_close')) if row.get('win_close') else None,
            'est_date': json.dumps(row.get('est_date')) if row.get('est_date') else None,
            'date_str': row.get('date_str'),
            'tags': json.dumps(row.get('tags')) if row.get('tags') else None,
            'slug': row.get('slug'),
            'media': json.dumps(row.get('media')) if row.get('media') else None,
            'result': row.get('result'),
            'suborbital': row.get('suborbital'),
            'modified': pd.to_datetime(row.get('modified')) if row.get('modified') else None,
            'type': launch_type
        }
        launch = Launch(**launch_data)
        session.merge(launch)
    session.commit()
    session.close()

def load_from_db():
    session = SessionLocal()
    upcoming_query = session.query(Launch).filter(Launch.type == 'upcoming')
    past_query = session.query(Launch).filter(Launch.type == 'past')
    upcoming_df = pd.read_sql(upcoming_query.statement, session.bind)
    past_df = pd.read_sql(past_query.statement, session.bind)
    session.close()
    return {'upcoming': upcoming_df, 'past': past_df}

def get_all_launches():
    # For simplicity, always fetch and save; in production, check timestamps
    print("Fetching data from API...")
    upcoming = get_upcoming_launches()
    past = get_past_launches()
    save_to_db(upcoming, 'upcoming')
    save_to_db(past, 'past')
    all_launches = {'upcoming': upcoming, 'past': past}
    return all_launches

if __name__ == '__main__':
    init_db()
    launches = get_all_launches()
    print(f"Upcoming launches: {len(launches['upcoming'])}")
    print(f"Past launches: {len(launches['past'])}")
    print("Upcoming launches DataFrame:")
    print(launches['upcoming'].head())
    print("Upcoming launches columns:", launches['upcoming'].columns.tolist())
    unique_providers = launches['upcoming']['provider'].apply(lambda x: x.get('name') if isinstance(x, dict) else x).unique().tolist()
    print("Unique providers:", unique_providers)
    print("Past launches DataFrame:")
    print(launches['past'].head())