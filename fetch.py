# import necessary libraries
import requests
import json
#import datetime
import pandas as pd
from os import environ

def define_params():
    params = dict()
    params['access_token'] = environ.get("FB_ACCESS_TOKEN")
    params['client_id'] = environ.get("FB_CLIENT_ID")
    params['client_secret'] = environ.get("FB_CLIENT_SECRET")
    params['graph_domain'] = 'https://graph.facebook.com'
    params['graph_version'] = 'v13.0'
    params['endpoint_base'] = params['graph_domain'] + '/' + params['graph_version'] + '/'
    params['instagram_account_id'] = environ.get("IG_ID")
    params['ig_username'] = environ.get("IG_USER")
    params['page_id'] = environ.get("FB_PAGE_ID")
    return params

def fetch_insights():
    params = define_params()
    url = params['endpoint_base'] + params['instagram_account_id'] + '/insights'
    endpointParams = dict()
    #endpointParams['fields'] = ['caption', 'like_count', 'comments']
    endpointParams['metric'] = ['impressions']
    endpointParams['period'] = ['day']
    endpointParams['access_token'] = params['access_token']

    # Requests Data
    req = requests.get(url, endpointParams )
    data = json.loads(req.content)

    imps = []
    dates = []
    while data['data'][0]['values'][0]['value'] > 0:
        imps.append(data['data'][0]['values'][1]['value'])
        imps.append(data['data'][0]['values'][0]['value'])
        dates.append(data['data'][0]['values'][1]['end_time'])
        dates.append(data['data'][0]['values'][0]['end_time'])
        data = json.loads(requests.get(data['paging']['previous']).content)

    df = pd.DataFrame()
    df['impressions'] = imps
    df['end_times'] = dates
    df['end_times'] = df['end_times'].apply(lambda x : x.split("T")[0])
    return df

def get_df():
    return fetch_insights()