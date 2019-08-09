from flask import Flask, render_template, send_file, jsonify, request, redirect, url_for
import  datetime
import os
import io
import numpy as np
import pandas as pd
import requests
import json
# import keras
# from keras.preprocessing import image
# from keras.preprocessing.image import img_to_array
# from keras.applications.xception import (Xception, preprocess_input, decode_predictions)
# from keras import backend as K

app = Flask(__name__)
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

########################
######DEFINE ROUTES#####
########################

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/LeSwishProphet")
def p1():
    import localize_data
    os.system('python localize_data.py')
    print("data updated @ ", datetime.datetime.now())
    return render_template("00p1.html")

@app.route("/EarthquakeTopology")
def p2():
    return render_template("00p2.html")

@app.route('/ImageProcessor/', methods=['GET', 'POST'])
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
