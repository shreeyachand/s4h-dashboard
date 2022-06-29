from flask import Flask, session, request, redirect, url_for, render_template
import fetch
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def home():
    mets = fetch.make_plots()
    return render_template("fig.html", metrics=mets)

@app.route("/post_engagement")
def eng():
    fetch.post_engagement()
    return render_template("eng.html")