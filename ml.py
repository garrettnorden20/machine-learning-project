import pandas as pd
import numpy as np
import xgboost as xgb
import sklearn as sci
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as pl
import shap


def seaborn_dataset_give():
    prefix = "data/archive/"
    matches = pd.read_csv(prefix + "matches.csv")
    participants = pd.read_csv(prefix + "participants.csv")
    champs = pd.read_csv(prefix + "champs.csv")

    stats1_1 = pd.read_csv(prefix + "stats1_1.csv", low_memory=False)
    stats1_2 = pd.read_csv(prefix + "stats1_2.csv", low_memory=False)
    stats1_3 = pd.read_csv(prefix + "stats1_3.csv", low_memory=False)
    stats1_4 = pd.read_csv(prefix + "stats1_4.csv", low_memory=False)
    stats2_1 = pd.read_csv(prefix + "stats2_1.csv", low_memory=False)
    stats2_2 = pd.read_csv(prefix + "stats2_2.csv", low_memory=False)
    stats2_3 = pd.read_csv(prefix + "stats2_3.csv", low_memory=False)
    stats = pd.concat([stats1_1, stats1_2, stats1_3, stats1_4, stats2_1, stats2_2, stats2_3])
    print(stats.shape)

    # merge into a single DataFrame
    allstats = pd.merge(participants, stats, how = 'left', on = ['id'], suffixes=('', '_y'))
    allstats = pd.merge(allstats, champs, how = 'left', left_on = 'championid', right_on = 'id', suffixes=('', '_y'))
    allstats = pd.merge(allstats, matches, how = 'left', left_on = 'matchid', right_on = 'id', suffixes=('', '_y'))

    allstats['adjposition'] = allstats.apply(final_position, axis=1)

    allstats['team'] = allstats['player'].apply(lambda x: '1' if x <= 5 else '2')
    allstats['team_role'] = allstats['team'] + ' - ' + allstats['adjposition']

    # convert to rates
    rate_features = [
        "kills", "deaths", "assists", "killingsprees", "doublekills",
        "triplekills", "quadrakills", "pentakills", "legendarykills",
        "totdmgdealt", "magicdmgdealt", "physicaldmgdealt", "truedmgdealt",
        "totdmgtochamp", "magicdmgtochamp", "physdmgtochamp", "truedmgtochamp",
        "totheal", "totunitshealed", "dmgtoobj", "timecc", "totdmgtaken",
        "magicdmgtaken", "physdmgtaken", "truedmgtaken", "goldearned", "goldspent",
        "totminionskilled", "neutralminionskilled", "ownjunglekills",
        "enemyjunglekills", "totcctimedealt", "pinksbought", "wardsplaced"
    ]
    for feature_name in rate_features:
        print(feature_name)
        allstats[feature_name] /= allstats["duration"] / 60  # per minute rate


    # remove matchid with duplicate roles, e.g. 3 MID in same team, etc
    remove_index = []
    for i in (
    '1 - MID', '1 - TOP', '1 - DUO_SUPPORT', '1 - DUO_CARRY', '1 - JUNGLE', '2 - MID', '2 - TOP', '2 - DUO_SUPPORT',
    '2 - DUO_CARRY', '2 - JUNGLE'):
        allstats_remove = allstats[allstats['team_role'] == i].groupby('matchid').agg({'team_role': 'count'})
        remove_index.extend(allstats_remove[allstats_remove['team_role'] != 1].index.values)

    # remove unclassified BOT, correct ones should be DUO_SUPPORT OR DUO_CARRY
    remove_index.extend(allstats[allstats['adjposition'] == 'BOT']['matchid'].unique())
    remove_index = list(set(remove_index))

    print('# matches in dataset before cleaning: {}'.format(allstats['matchid'].nunique()))
    allstats = allstats[~allstats['matchid'].isin(remove_index)]
    print('# matches in dataset after cleaning: {}'.format(allstats['matchid'].nunique()))
    return allstats

def final_position(row):
    if row['role'] in ('DUO_SUPPORT', 'DUO_CARRY'):
        return row['role']
    else:
        return row['position']


def logistic_regression(X, y):
    Xt, Xv, yt, yv = train_test_split(X, y, test_size=0.2, random_state=10)
    LR = sci.linear_model.LogisticRegression(random_state=0, solver='lbfgs', multi_class='ovr').fit(Xt, yt)
    LR.predict(Xv)
    round(LR.score(Xv, yv), 4)
    return round(LR.score(Xv, yv), 4)

