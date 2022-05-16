from flask import Flask, session, request, redirect, url_for, render_template
import fetch
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def hello_world():
    data = fetch.get_df()
    plt.scatter(data['end_times'],data['impressions'])
    plt.savefig("static/graph.png")
    plt.close() 
    return render_template("fig.html")