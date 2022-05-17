from flask import Flask, session, request, redirect, url_for, render_template
import fetch
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def hello_world():
    data = fetch.get_df()
    plt.plot(data['end_times'],data['impressions'])
    plt.title("@studentsforhans IG impressions this week")
    plt.xlabel("date")
    plt.ylabel("impressions")
    # REMEMBER IT's END TIME T7????
    plt.savefig("static/graph.png")
    plt.close() 
    return render_template("fig.html")