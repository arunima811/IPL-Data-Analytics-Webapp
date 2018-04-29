from flask import Flask, render_template, make_response
import numpy as np
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from utils import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from io import BytesIO
import random

score_df = pd.read_csv("data/deliveries.csv")
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/batsman-analysis-1")
def batsmananalysis1():
    temp_df = score_df.groupby('batsman')['batsman_runs'].agg('sum').reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
    temp_df = temp_df.iloc[:10,:]

    labels = np.array(temp_df['batsman'])
    ind = np.arange(len(labels))
    width = 0.9
    fig, ax = plt.subplots()
    rects = ax.bar(ind, np.array(temp_df['batsman_runs']), width=width, color='blue')
    ax.set_xticks(ind+((width)/2.))
    ax.set_xticklabels(labels, rotation='vertical')
    ax.set_ylabel("Count")
    ax.set_title("Top run scorers in IPL")
    autolabel(rects,ax)
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/batsman-analysis-4s")
def batsmananalysis4s():
    temp_df = score_df.groupby('batsman')['batsman_runs'].agg(lambda x: (x==4).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
    temp_df = temp_df.iloc[:10,:]

    labels = np.array(temp_df['batsman'])
    ind = np.arange(len(labels))
    width = 0.9
    fig, ax = plt.subplots()
    rects = ax.bar(ind, np.array(temp_df['batsman_runs']), width=width, color='green')
    ax.set_xticks(ind+((width)/2.))
    ax.set_xticklabels(labels, rotation='vertical')
    ax.set_ylabel("Count")
    ax.set_title("Batsman with most number of boundaries(fours)!")
    autolabel(rects,ax)
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/batsman-analysis-6s")
def batsmananalysis6s():
    temp_df = score_df.groupby('batsman')['batsman_runs'].agg(lambda x: (x==6).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
    temp_df = temp_df.iloc[:10,:]

    labels = np.array(temp_df['batsman'])
    ind = np.arange(len(labels))
    width = 0.9
    fig, ax = plt.subplots()
    rects = ax.bar(ind, np.array(temp_df['batsman_runs']), width=width, color='m')
    ax.set_xticks(ind+((width)/2.))
    ax.set_xticklabels(labels, rotation='vertical')
    ax.set_ylabel("Count")
    ax.set_title("Batsman with most number of sixes.!")
    autolabel(rects,ax)
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/batsman-analysis-0s")
def batsmananalysis0s():
    temp_df = score_df.groupby('batsman')['batsman_runs'].agg(lambda x: (x==0).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
    temp_df = temp_df.iloc[:10,:]

    labels = np.array(temp_df['batsman'])
    ind = np.arange(len(labels))
    width = 0.9
    fig, ax = plt.subplots()
    rects = ax.bar(ind, np.array(temp_df['batsman_runs']), width=width, color='c')
    ax.set_xticks(ind+((width)/2.))
    ax.set_xticklabels(labels, rotation='vertical')
    ax.set_ylabel("Count")
    ax.set_title("Batsman with most number of dot balls.!")
    autolabel(rects,ax)
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/batsman-analysis-dotperct")
def batsmananalysisdotperct():
    temp_df = score_df.groupby('batsman')['batsman_runs'].agg([balls_faced, dot_balls]).reset_index()
    temp_df = temp_df.ix[temp_df.balls_faced>200,:]
    temp_df['percentage_of_dot_balls'] = (temp_df['dot_balls'] / temp_df['balls_faced'])*100.
    temp_df = temp_df.sort_values(by='percentage_of_dot_balls', ascending=False).reset_index(drop=True)
    temp_df = temp_df.iloc[:10,:]

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    labels = np.array(temp_df['batsman'])
    ind = np.arange(len(labels))
    width = 0.9
    rects = ax1.bar(ind, np.array(temp_df['dot_balls']), width=width, color='brown')
    ax1.set_xticks(ind+((width)/2.))
    ax1.set_xticklabels(labels, rotation='vertical')
    ax1.set_ylabel("Count of dot balls", color='brown')
    ax1.set_title("Batsman with highest percentage of dot balls (balls faced > 200)")
    ax2.plot(ind+0.45, np.array(temp_df['percentage_of_dot_balls']), color='b', marker='o')
    ax2.set_ylabel("Percentage of dot balls", color='b')
    ax2.set_ylim([0,100])
    ax2.grid(b=False)
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/bowler-analysis")
def bowleranalysis():
    temp_df = score_df.groupby('bowler')['ball'].agg('count').reset_index().sort_values(by='ball', ascending=False).reset_index(drop=True)
    temp_df = temp_df.iloc[:10,:]
    labels = np.array(temp_df['bowler'])
    ind = np.arange(len(labels))
    width = 0.9
    fig, ax = plt.subplots()
    rects = ax.bar(ind, np.array(temp_df['ball']), width=width, color='cyan')
    ax.set_xticks(ind+((width)/2.))
    ax.set_xticklabels(labels, rotation='vertical')
    ax.set_ylabel("Count")
    ax.set_title("Top Bowlers - Number of balls bowled in IPL")
    autolabel(rects,ax)
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/bowler-analysis-mostdots")
def bowleranalysismostdots():
    temp_df = score_df.groupby('bowler')['total_runs'].agg(lambda x: (x==0).sum()).reset_index().sort_values(by='total_runs', ascending=False).reset_index(drop=True)
    temp_df = temp_df.iloc[:10,:]
    labels = np.array(temp_df['bowler'])
    ind = np.arange(len(labels))
    width = 0.9
    fig, ax = plt.subplots()
    rects = ax.bar(ind, np.array(temp_df['total_runs']), width=width, color='yellow')
    ax.set_xticks(ind+((width)/2.))
    ax.set_xticklabels(labels, rotation='vertical')
    ax.set_ylabel("Count")
    ax.set_title("Top Bowlers - Number of dot balls bowled in IPL")
    autolabel(rects,ax)
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/bowler-analysis-mostextras")
def bowleranalysismostextras():
    temp_df = score_df.groupby('bowler')['extra_runs'].agg(lambda x: (x>0).sum()).reset_index().sort_values(by='extra_runs', ascending=False).reset_index(drop=True)
    temp_df = temp_df.iloc[:10,:]
    labels = np.array(temp_df['bowler'])
    ind = np.arange(len(labels))
    width = 0.9
    fig, ax = plt.subplots()
    rects = ax.bar(ind, np.array(temp_df['extra_runs']), width=width, color='magenta')
    ax.set_xticks(ind+((width)/2.))
    ax.set_xticklabels(labels, rotation='vertical')
    ax.set_ylabel("Count")
    ax.set_title("Bowlers with more extras in IPL")
    autolabel(rects,ax)
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == "__main__":
    app.run(debug=True)
