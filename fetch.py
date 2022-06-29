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
    return df, desc

def cat_insights(metric):
    params = define_params()
    url = params['endpoint_base'] + params['instagram_account_id'] + '/insights'
    endpointParams = dict()
    endpointParams['metric'] = [metric]
    endpointParams['period'] = ['lifetime']
    endpointParams['access_token'] = params['access_token']
    data = json.loads(requests.get(url, endpointParams).content)
    
    info = data['data'][0]['values'][0]['value']
    return info

def make_plots():
    metrics = ['impressions', 'reach', 'profile_views', 'follower_count']
    for met in metrics:
        #plt.ioff()
        data, desc = fetch_insights(met)
        #desc = desc.replace("number of","#").split(" the Business Account's ")
        plt.plot(data['end_times'],data['vals'])
        #plt.title(desc[0] + " @studentsforhans " + desc[1])
        plt.title(desc)
        plt.xlabel("date")
        plt.ylabel(met)
        # REMEMBER IT's END TIME T7????
        plt.savefig("static/" + met + ".jpg")
        plt.close()
    metrics2 = ['audience_gender_age', 'audience_city']
    for met in metrics2:
        demog = cat_insights(met)
        ks = list(demog.keys())
        for x in ks:
            demog[x.replace(", Maryland", "")] = demog.pop(x)
        demog = dict(sorted(demog.items(), key=lambda x: x[1]))
        plt.rc('ytick', labelsize=7) 
        plt.barh(list(demog.keys()), demog.values())
        plt.title(met)
        plt.xlabel("followers")
        plt.ylabel("group")
        plt.savefig("static/" + met + ".jpg",bbox_inches='tight')
        plt.close()
    return metrics + metrics2

def post_engagement():
    params = define_params()
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media'
    endpointParams = dict()
    endpointParams['fields'] = ['caption']
    endpointParams['access_token'] = params['access_token']
    data = requests.get(url, endpointParams )
    media = json.loads(data.content)
    rates = []
    for i in media['data']:
        url = params['endpoint_base'] + i['id'] + '/insights'
        endpointParams = dict()
        endpointParams['metric'] = 'reach,engagement'
        endpointParams['access_token'] = params['access_token']
        data = requests.get(url, endpointParams)
        p = json.loads(data.content)
        if 'data' in p.keys() and p['data'][0]['values'][0]['value'] > 0:
            rates.append([ p['data'][1]['values'][0]['value']/p['data'][0]['values'][0]['value'], i['caption'][:15]])
    df = pd.DataFrame(rates[::-1],columns=["eng_rate", "caption"])
    plt.plot(df['eng_rate'])
    plt.xticks(list(range(len(df))),df['caption'],rotation=90)
    plt.xlabel('caption')
    plt.ylabel('engagement rate (likes+comments/# unique views)')
    plt.savefig("static/" + 'eng_rate' + ".jpg", bbox_inches='tight')
    plt.close()