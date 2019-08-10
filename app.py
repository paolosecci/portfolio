from flask import Flask, render_template, send_file, jsonify, request, redirect, url_for

import datetime
import os
import io
import numpy as np
import requests
import json
# import keras
# from keras.preprocessing import image
# from keras.preprocessing.image import img_to_array
# from keras.applications.xception import (Xception, preprocess_input, decode_predictions)
# from keras import backend as K
#from flask_pymongo import PyMongo

#NBA
import pandas as pd

#Hawaii
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#vegan user agent
this_user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}


# #functions
# def load_model():
#     global model
#     global graph
#     model = Xception(weights="imagenet")
#     graph = K.get_session().graph
# def prepare_image(img):
#     img = img_to_array(img)
#     img = np.expand_dims(img, axis=0)
#     img = preprocess_input(img)
#     #return processed image
#     return img
# #call functions and set vars
# load_model()
# app.config['UPLOAD_FOLDER'] = 'Uploads'
# model = None
# graph = None

#for BioDiversity
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Samples_Metadata = Base.classes.sample_metadata
Samples = Base.classes.samples

########################
######DEFINE ROUTES#####
########################

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/BioDiversity")
def index():
    """Return the homepage."""
    return render_template("00p5.html")

@app.route("/BioDiversity/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])


@app.route("/BioDiversity/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/BioDiversity/samples/<sample>")
def samples(sample):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    # Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)

# #for HAwaii Demo
# def query_start_date(i):
#     # Calculate the date 1 year ago from today
#     now = datetime.datetime.now() #get NOW (datetime objects are not writable)
#     if now.month > 9:
#         search_start_date = str(now.year - i) + '-' + str(now.month) + '-' + str(now.day) #format to query data
#     else:
#         search_start_date = str(now.year - i) + '-0' + str(now.month) + '-' + str(now.day) #format to query data
#
#     #get most recent date
#     #most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
#
#     return search_start_date
#
# def create_plots(df, considered_data, most_recent_date):
#     import matplotlib.pyplot as plt
#     # Use Pandas Plotting with Matplotlib to plot the data
#     df.plot(use_index=True, y='prcp', figsize=(10,7))
#     plt.title("Avg Precipitation in Hawaii by Date", fontweight='bold',size=10)
#     plt.xlabel(f"Date Range:  {considered_data} - {most_recent_date}", fontweight='bold', size=9)
#     plt.ylabel("Precipitation (inches)", fontweight='bold', size=9)
#     plt.legend(['precipitation'])
#     plt.tight_layout()
#
#     # Rotate the xticks for the dates
#     plt.yticks(size=7)
#     plt.xticks(rotation=45, size=7)
#
#     plt.savefig('precipitation_amounts.png')
#     return
#
# @app.route("/Hawaii")
# def p5():
#     ######LINK DB######
#     #setup data_engine
#     engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#     #create base from model
#     Base = automap_base()
#     #reflect tables
#     Base.prepare(engine, reflect=True)
#     Base.classes.keys()
#     #create references to each table
#     Measurement = Base.classes.measurement
#     Station = Base.classes.station
#     #link py to db
#     session = Session(engine)
#     #set inspector
#     inspector = inspect(engine)
#     ######DB LINKED########
#
#     from matplotlib import style
#     style.use('fivethirtyeight')
#
#     #inspect!!!
#     inspector = inspect(engine)
#
#     for table_name in inspector.get_table_names():
#         for column in inspector.get_columns(table_name):
#             print( table_name, "\t", column.get('name'), column.get('type'))
#
#     #num_in = input("enter the number of years of data you would like to analyze: ")
#     considered_data = query_start_date(7)
#     #get most recent date
#     most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
#
#     #retrieve the data and precipitation scores with session.query()
#     print('retrieving the data and precipitation scores with session query...')
#     re = session.query(Measurement.date, Measurement.prcp)
#
#     #filter via 7 years
#     re = re.filter(Measurement.date >= considered_data)
#
#     #first create dictionary to give to pandas
#     dict_for_df = {
#         'date': [],
#         'prcp': []
#     }
#
#     #populate dictionary with results from query
#     for row in re:
#         dict_for_df['date'].append(row.date)
#         dict_for_df['prcp'].append(row.prcp)
#
#     #make df from dict_for_df
#     df = pd.DataFrame(dict_for_df)
#
#     #sort, index, clean the df
#     df = df.sort_values(['date']).set_index(['date']).dropna()
#
#     create_plots(df, considered_data, most_recent_date)
#
#     #STATS summary
#     summary_dict = {
#         'count': df.count(),
#         'mean': df.mean(),
#         'std_dev': df.std(),
#         'min': df.min(),
#         'Q1': df.quantile(.25),
#         'median': df.median(),
#         'Q3': df.quantile(.75),
#         'max': df.max()
#     }
#     summary_df = pd.DataFrame(summary_dict)
#
#     ### GOOD WAY
#     return jsonify(summary_dict)
#
# @app.route("/Hawaii/api/v1.2/precipitation") #precipitation
# def precipitation():
#
#     "Queries for the dates and temperature observations since 1 Jan 2017"
#
#     #query for dates and tobs
#     prcp_re = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2017-01-01').all()
#
#     #create dictionary of lists, fill list
#     prcp_dict = {
#         'date': [],
#         'tobs': [],
#     }
#     for prcp in prcp_re:
#         prcp_dict['date'].append(Measurement.date)
#         prcp_dict['tobs'].append(Measurement.tobs)
#
#     prcp_json = jsonify(prcp_dict)
#     return prcp_json
#
# @app.route("/Hawaii/api/v1.2/stations") #stations
# def stations():
#
#     "Returns a JSON list of stations from the dataset"
#
#     station_re = session.query(Station.station).all()
#
#     station_list = []
#     for row in station_re:
#         station_list.append(row.station)
#
#     stations_json = jsonify(station_list)
#     return stations_json
#
# @app.route("/Hawaii/api/v1.2/tobs") #tobs
# def tobs():
#
#     "Returns a JSON list of Temperature Observations (tobs) since 1 Jan 2017"
#
#     tobs_re = session.query(Measurement.tobs).filter(Measurement.date > '2017-01-01').all()
#
#     tobs_list = []
#     for row in tobs_re:
#         tobs_list.append(row.tobs)
#
#     tobs_json = jsonify(tobs_list)
#     return tobs_json
#
# @app.route("/Hawaii/api/v1.2/<start>") #start
# def start(start):
#
#     "Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start"
#
#     s_re_uf = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
#     s_re = s_re_uf.filter(Measurement.date >= start)
#
#     s_dict = {
#         'min': s_re[0][0],
#         'mean': s_re[0][1],
#         'max': s_re[0][2]
#     }
#
#     s_json = jsonify(s_dict)
#     return s_json
#
# @app.route("/Hawaii/api/v1.2/<start>/<end>") #start/end
# def start_end(start, end):
#
#     "Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end"
#
#     se_re_uf = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
#     se_re = se_re_uf.filter(Measurement.date >= start).filter(Measurement.date <= end)
#
#     se_dict = {
#         'min': se_re[0][0],
#         'mean': se_re[0][1],
#         'max': se_re[0][2]
#     }
#
#     se_json = jsonify(se_dict)
#     return se_json
#
# @app.route("/AresMission/scrape")
# def scraper():
#     mars_data = mongo.db.mars_data
#     mars_webscrape_re = mission_to_mars.scrape()
#     mars_data.update({}, mars_webscrape_re, upsert=True)
#     return redirect("/AresMission", code=302)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Samples_Metadata = Base.classes.sample_metadata
Samples = Base.classes.samples

@app.route("/LeSwishProphet")
def p1():
    #import localize_data
    #os.system('python localize_data.py')
    print("data updated @ ", datetime.datetime.now())
    return render_template("00p1.html")

@app.route("/QuakeTopology")
def p2():
    return render_template("00p2.html")

@app.route('/Barad-Dûr/', methods=['GET', 'POST'])
def p3():
    # data = {"success": False}
    # if request.method == 'POST':
    #     if request.files.get('file'):
    #         #read input file
    #         file = request.files['file']
    #         #read filename
    #         filename = file.filename
    #         #create os path to uploads directory
    #         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #         file.save(filepath)
    #         #load the saved image and resize to the Xception 299x299 pixels
    #         image_size = (299, 299)
    #         im = keras.preprocessing.image.load_img(filepath,target_size=image_size,grayscale=False)
    #         #preprocess the image for classification
    #         image = prepare_image(im)
    #         global graph
    #         with graph.as_default():
    #             preds = model.predict(image)
    #             res = decode_predictions(preds)
    #             #print the res
    #             print(res)
    #             data["predictions"] = []
    #             #loop over the results and add to returned predictions
    #             for (imagenetID, label, prob) in results[0]:
    #                 r = {"label": label, "probability": float(prob)}
    #                 data["predictions"].append(r)
    #             #store boolean for process success
    #             data["success"] = True
    #     return jsonify(data)

    return render_template("00p3.html")

@app.route("/Batcave")
def p4():
    return render_template("00p4.html")

@app.route("/resume2019")
def resume():
    return send_file('static/tank/PSResume.pdf')


#for LeSwishProphet Demo
import pandas as pd
import requests
import json
this_user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
def clean_df(df):
    df = df.drop(columns=['SEASON_ID', 'PLAYER_ID', 'TEAM_ID','VIDEO_AVAILABLE'])
    df['GAME_DATE'] = df['GAME_DATE'].astype(str)
    return df
def make_days_since_col(df):
    dates = df['GAME_DATE']
    days_since_arr = []
    for i in dates:
        days_since_arr.append(get_time_ellapsed(i))
    df['DAYS_SINCE_RN'] = days_since_arr
    last_game = df['DAYS_SINCE_RN'][0]
    df['DAYS_SINCE_RN'] = df['DAYS_SINCE_RN'] - last_game
    return df
def get_time_ellapsed(str_date):
    ymd = str_date.split('-')
    y = int(ymd[0])
    m = int(ymd[1])
    d = int(ymd[2])
    then = datetime.datetime(y,m,d)
    rn = datetime.datetime.now()
    delta = rn - then
    return delta.days
def get_team_df(team, df):
    team_df = df[df['TEAM_ABBREVIATION']==team]
    return team_df
def get_player_df(player, df):
    player_df = df[df['PLAYER_NAME']==player]
    return player_df
def predict_lineup(team_df):
    lineup_df = team_df[team_df['DAYS_SINCE_RN']<=7]
    players = lineup_df['PLAYER_NAME'].unique()
    lineup_out = {}
    for player in players:
        player_df = lineup_df[lineup_df['PLAYER_NAME'] == player]
        lineup_out[player] = player_df['MIN'].mean()
    import operator
    line_up_sorted_12 = list(reversed(sorted(lineup_out.items(), key=operator.itemgetter(1))))[:12]
    lineup = []
    for obj in line_up_sorted_12:
        lineup.append(obj[0])
    return lineup
def predict_stat(player, stat, df):
    player_df = get_player_df(player, df)
    sum_days = 0
    for num_days in player_df['DAYS_SINCE_RN']:
        sum_days += num_days
    importances = []
    for num_days in player_df['DAYS_SINCE_RN']:
        importance = ((sum_days - num_days)/sum_days)
        importances.append(importance**4)
    sum_days
    stat_ser = player_df[stat]
    stats = []
    for stat in stat_ser:
        stats.append(int(stat))
    scores = []
    for i in range(len(stats)):
        score = importances[i]*stats[i]
        scores.append(score)
    sum_importance = 0
    for imp in importances:
        sum_importance += imp
    if (sum_importance == 0):
        return sum(scores)
    else:
        p_stat = sum(scores)/sum_importance
        return round(p_stat, 2)
def make_json_df(nba_json):
    headers = nba_json['resultSets'][0]['headers']
    data = nba_json['resultSets'][0]['rowSet']
    df = pd.DataFrame(data, columns=headers)
    return df
def predict_team(t):
    with open('data/nba_team_boxscores.json') as file_in:
        nba_t_json = json.load(file_in)
    df = make_json_df(nba_t_json)
    t_df = df[df['TEAM_ABBREVIATION'] == t]
    t_games = list(t_df['GAME_ID'])
    t_match_df = df[df['GAME_ID'].isin(t_games)]
    t_opp_df = t_match_df[t_match_df['TEAM_ABBREVIATION'] != t]
    t_opp_pts = list(t_opp_df['PTS'])
    t_pts = t_df['PTS']
    while len(t_opp_pts) < len(t_df):
        t_opp_pts.append(sum(t_opp_pts)/len(t_opp_pts))
    pts_list = []
    for pts in t_df['PTS']:
        pts_list.insert(0, pts)
    t_df['pts_r'] = pts_list
    o_pts_list = []
    for o_pts in t_opp_pts:
        o_pts_list.insert(0, o_pts)
    t_df['o_pts_r'] = o_pts_list
    predicted_pts = t_df['pts_r'].ewm(alpha=.5).mean().iloc[-1]
    predicted_opp_pts = t_df['o_pts_r'].ewm(alpha=.5).mean().iloc[-1]
    return {'predicted_pts': predicted_pts, 'predicted_opp_pts': predicted_opp_pts}
@app.route("/predict/<team>")
def predict(team):
    with open('data/nba_player_boxscores.json') as file_in:
    	nba_json = json.load(file_in)
    df = clean_df(make_json_df(nba_json))
    df = make_days_since_col(df)
    team_df = get_team_df(team, df)
    team_lineup = predict_lineup(team_df)
    p_json_out = []
    sum_pts = 0
    for player in team_lineup:
        p_pts = predict_stat(player, 'PTS', team_df)
        p_json_out.append({
            'NAME': player,
            'PTS': p_pts,
            'AST': predict_stat(player, 'AST', team_df),
            'REB': predict_stat(player, 'REB', team_df)
        })
        sum_pts += p_pts
    json_out = [sum_pts, p_json_out]
    return jsonify(json_out)
@app.route('/simgame/<team1>/<team2>')
def simgame(team1, team2):
    p_t1 = predict_team(team1)
    p_t2 = predict_team(team2)
    t1s = (p_t1['predicted_pts'] + p_t2['predicted_opp_pts']) / 2
    t2s = (p_t2['predicted_pts'] + p_t1['predicted_opp_pts']) / 2
    return jsonify([t1s, t2s])

if __name__ == "__main__":
    app.run(debug=True)
