from flask import Flask, render_template
from models import init_db, SessionLocal, Launch
import pandas as pd
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    session = SessionLocal()
    upcoming_count = session.query(Launch).filter(Launch.type == 'upcoming').count()
    past_count = session.query(Launch).filter(Launch.type == 'past').count()
    session.close()
    return render_template('index.html', upcoming_count=upcoming_count, past_count=past_count)

@app.route('/launches')
def launches():
    session = SessionLocal()
    launches = session.query(Launch).all()
    for launch in launches:
        if launch.provider:
            p_dict = json.loads(launch.provider)
            launch.provider_name = p_dict.get('name', 'Unknown')
        else:
            launch.provider_name = 'Unknown'
    session.close()
    return render_template('launches.html', launches=launches)

@app.route('/launches/upcoming')
def upcoming():
    session = SessionLocal()
    launches = session.query(Launch).filter(Launch.type == 'upcoming').all()
    for launch in launches:
        if launch.provider:
            p_dict = json.loads(launch.provider)
            launch.provider_name = p_dict.get('name', 'Unknown')
        else:
            launch.provider_name = 'Unknown'
    session.close()
    return render_template('launches.html', launches=launches)

@app.route('/launches/past')
def past():
    session = SessionLocal()
    launches = session.query(Launch).filter(Launch.type == 'past').all()
    for launch in launches:
        if launch.provider:
            p_dict = json.loads(launch.provider)
            launch.provider_name = p_dict.get('name', 'Unknown')
        else:
            launch.provider_name = 'Unknown'
    session.close()
    return render_template('launches.html', launches=launches)

@app.route('/providers')
def providers():
    session = SessionLocal()
    # Since provider is JSON, extract names
    results = session.query(Launch.provider).filter(Launch.type == 'upcoming').all()
    providers = set()
    for (p,) in results:
        if p:
            p_dict = json.loads(p)
            if 'name' in p_dict:
                providers.add(p_dict['name'])
    session.close()
    return render_template('providers.html', providers=list(providers))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5002)))
