# import necessary libraries
import requests
import json
#import datetime
import pandas as pd
from os import environ
import numpy as np
import matplotlib.pyplot as plt

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

def fetch_insights(metric):
    params = define_params()
    url = params['endpoint_base'] + params['instagram_account_id'] + '/insights'
    endpointParams = dict()
    #endpointParams['fields'] = ['caption', 'like_count', 'comments']
    endpointParams['metric'] = [metric]
    endpointParams['period'] = ['day']
    endpointParams['access_token'] = params['access_token']

    # Requests Data
    req = requests.get(url, endpointParams )
    data = json.loads(req.content)
    desc = data['data'][0]['description']
    vals = []
    dates = []
    i = 0
    while i < 4:
        vals.append(data['data'][0]['values'][1]['value'])
        vals.append(data['data'][0]['values'][0]['value'])
        dates.append(data['data'][0]['values'][1]['end_time'].split("T")[0].split("022-")[1])
        dates.append(data['data'][0]['values'][0]['end_time'].split("T")[0].split("022-")[1])
        data = json.loads(requests.get(data['paging']['previous']).content)
        i+=1

    df = pd.DataFrame()
    df['vals'] = vals[::-1]
    df['end_times'] = dates[::-1]
    #df['end_times'] = df['end_times'].apply(lambda x : x.split("T")[0])
    return df, desc

def make_plots():
    metrics = ['impressions', 'reach', 'profile_views']
    for met in metrics:
        #plt.ioff()
        data, desc = fetch_insights(met)
        desc = desc.replace("number of","#").split(" the Business Account's ")
        plt.plot(data['end_times'],data['vals'])
        plt.title(desc[0] + " @studentsforhans " + desc[1])
        plt.xlabel("date")
        plt.ylabel(met)
        # REMEMBER IT's END TIME T7????
        plt.savefig("static/" + met + ".jpg")
        plt.close() 
    return metrics