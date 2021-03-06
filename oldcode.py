import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as pl
import shap

def get_main_frame():
    print("BEGIN")
    prefix = "data/archive/"
    matches = pd.read_csv(prefix+"matches.csv")
    participants = pd.read_csv(prefix+"participants.csv")

    stats1_1 = pd.read_csv(prefix+"stats1_1.csv", low_memory=False)
    stats1_2 = pd.read_csv(prefix+"stats1_2.csv", low_memory=False)
    stats1_3 = pd.read_csv(prefix+"stats1_3.csv", low_memory=False)
    stats1_4 = pd.read_csv(prefix+"stats1_4.csv", low_memory=False)
    stats2_1 = pd.read_csv(prefix+"stats2_1.csv", low_memory=False)
    stats2_2 = pd.read_csv(prefix+"stats2_2.csv", low_memory=False)
    stats2_3 = pd.read_csv(prefix+"stats2_3.csv", low_memory=False)
    stats = pd.concat([stats1_1,stats1_2,stats1_3,stats1_4,stats2_1,stats2_2,stats2_3])

    # merge into a single DataFrame
    a = pd.merge(participants, matches, left_on="matchid", right_on="id")
    allstats_orig = pd.merge(a, stats, left_on="matchid", right_on="id")
    allstats = allstats_orig.copy()

    # drop games that lasted less than 15 minutes
    print(len(allstats))
    allstats = allstats.loc[allstats["duration"] >= 10*60,:]
    print(len(allstats))

    # Convert string-based categories to numeric values
    cat_cols = ["role", "position", "version", "platformid"]
    for c in cat_cols:
        allstats[c] = allstats[c].astype('category')
        allstats[c] = allstats[c].cat.codes
    allstats["wardsbought"] = allstats["wardsbought"].astype(np.int32)

    # convert all features we want to consider as rates
    rate_features = [
        "kills", "deaths", "assists", "killingsprees", "doublekills",
        "triplekills", "quadrakills", "pentakills", "legendarykills",
        "totdmgdealt", "magicdmgdealt", "physicaldmgdealt", "truedmgdealt",
        "totdmgtochamp", "magicdmgtochamp", "physdmgtochamp", "truedmgtochamp",
        "totheal", "totunitshealed", "dmgtoobj", "timecc", "totdmgtaken",
        "magicdmgtaken", "physdmgtaken", "truedmgtaken", "goldearned", "goldspent",
        "totminionskilled", "neutralminionskilled", "ownjunglekills",
        "enemyjunglekills", "totcctimedealt", "pinksbought", "wardsbought",
        "wardsplaced", "wardskilled"
    ]
    for feature_name in rate_features:
        allstats[feature_name] /= allstats["duration"] / 60  # per minute rate

    # convert to fraction of game
    allstats["longesttimespentliving"] /= allstats["duration"]

    # define friendly names for the features
    full_names = {
        "kills": "Kills per min.",
        "deaths": "Deaths per min.",
        "assists": "Assists per min.",
        "killingsprees": "Killing sprees per min.",
        "longesttimespentliving": "Longest time living as % of game",
        "doublekills": "Double kills per min.",
        "triplekills": "Triple kills per min.",
        "quadrakills": "Quadra kills per min.",
        "pentakills": "Penta kills per min.",
        "legendarykills": "Legendary kills per min.",
        "totdmgdealt": "Total damage dealt per min.",
        "magicdmgdealt": "Magic damage dealt per min.",
        "physicaldmgdealt": "Physical damage dealt per min.",
        "truedmgdealt": "True damage dealt per min.",
        "totdmgtochamp": "Total damage to champions per min.",
        "magicdmgtochamp": "Magic damage to champions per min.",
        "physdmgtochamp": "Physical damage to champions per min.",
        "truedmgtochamp": "True damage to champions per min.",
        "totheal": "Total healing per min.",
        "totunitshealed": "Total units healed per min.",
        "dmgtoobj": "Damage to objects per min.",
        "timecc": "Time spent with crown control per min.",
        "totdmgtaken": "Total damage taken per min.",
        "magicdmgtaken": "Magic damage taken per min.",
        "physdmgtaken": "Physical damage taken per min.",
        "truedmgtaken": "True damage taken per min.",
        "goldearned": "Gold earned per min.",
        "goldspent": "Gold spent per min.",
        "totminionskilled": "Total minions killed per min.",
        "neutralminionskilled": "Neutral minions killed per min.",
        "ownjunglekills": "Own jungle kills per min.",
        "enemyjunglekills": "Enemy jungle kills per min.",
        "totcctimedealt": "Total crown control time dealt per min.",
        "pinksbought": "Pink wards bought per min.",
        "wardsbought": "Wards bought per min.",
        "wardsplaced": "Wards placed per min.",
        "turretkills": "# of turret kills",
        "inhibkills": "# of inhibitor kills",
        "dmgtoturrets": "Damage to turrets"
    }
    feature_names = [full_names.get(n, n) for n in allstats.columns]
    allstats.columns = feature_names

    return allstats

def get_X_Y():
    print("BEGIN LOL3qwc")
    prefix = "data/archive/"
    matches = pd.read_csv(prefix + "matches.csv", engine='python')
    participants = pd.read_csv(prefix + "participants.csv", engine='python')

    '''
    stats1_1 = pd.read_csv(prefix + "stats1_1.csv", low_memory=False)
    stats1_2 = pd.read_csv(prefix + "stats1_2.csv", low_memory=False)
    stats1_3 = pd.read_csv(prefix + "stats1_3.csv", low_memory=False)
    stats1_4 = pd.read_csv(prefix + "stats1_4.csv", low_memory=False)
    stats2_1 = pd.read_csv(prefix + "stats2_1.csv", low_memory=False)
    stats2_2 = pd.read_csv(prefix + "stats2_2.csv", low_memory=False)
    stats2_3 = pd.read_csv(prefix + "stats2_3.csv", low_memory=False)
    stats = pd.concat([stats1_1, stats1_2, stats1_3, stats1_4, stats2_1, stats2_2, stats2_3])
    '''
    stats1 = pd.read_csv(prefix+"stats1.csv", engine='python', error_bad_lines=False)
    stats2 = pd.read_csv(prefix+"stats2.csv", engine='python', error_bad_lines=False)
    stats = pd.concat([stats1,stats2])


    # merge into a single DataFrame
    a = pd.merge(participants, matches, left_on="matchid", right_on="id")
    allstats_orig = pd.merge(a, stats, left_on="matchid", right_on="id")
    allstats = allstats_orig.copy()

    # drop games that lasted less than 10 minutes
    allstats = allstats.loc[allstats["duration"] >= 10 * 60, :]

    # Convert string-based categories to numeric values
    cat_cols = ["role", "position", "version", "platformid"]
    for c in cat_cols:
        allstats[c] = allstats[c].astype('category')
        allstats[c] = allstats[c].cat.codes
    allstats["wardsbought"] = allstats["wardsbought"].astype(np.int32)

    X = allstats.drop(["win"], axis=1)
    y = allstats["win"]

    # convert all features we want to consider as rates
    rate_features = [
        "kills", "deaths", "assists", "killingsprees", "doublekills",
        "triplekills", "quadrakills", "pentakills", "legendarykills",
        "totdmgdealt", "magicdmgdealt", "physicaldmgdealt", "truedmgdealt",
        "totdmgtochamp", "magicdmgtochamp", "physdmgtochamp", "truedmgtochamp",
        "totheal", "totunitshealed", "dmgtoobj", "timecc", "totdmgtaken",
        "magicdmgtaken", "physdmgtaken", "truedmgtaken", "goldearned", "goldspent",
        "totminionskilled", "neutralminionskilled", "ownjunglekills",
        "enemyjunglekills", "totcctimedealt", "pinksbought", "wardsbought",
        "wardsplaced", "wardskilled"
    ]
    for feature_name in rate_features:
        X[feature_name] /= X["duration"] / 60  # per minute rate

    # convert to fraction of game
    X["longesttimespentliving"] /= X["duration"]

    # define friendly names for the features
    full_names = {
        "kills": "Kills per min.",
        "deaths": "Deaths per min.",
        "assists": "Assists per min.",
        "killingsprees": "Killing sprees per min.",
        "longesttimespentliving": "Longest time living as % of game",
        "doublekills": "Double kills per min.",
        "triplekills": "Triple kills per min.",
        "quadrakills": "Quadra kills per min.",
        "pentakills": "Penta kills per min.",
        "legendarykills": "Legendary kills per min.",
        "totdmgdealt": "Total damage dealt per min.",
        "magicdmgdealt": "Magic damage dealt per min.",
        "physicaldmgdealt": "Physical damage dealt per min.",
        "truedmgdealt": "True damage dealt per min.",
        "totdmgtochamp": "Total damage to champions per min.",
        "magicdmgtochamp": "Magic damage to champions per min.",
        "physdmgtochamp": "Physical damage to champions per min.",
        "truedmgtochamp": "True damage to champions per min.",
        "totheal": "Total healing per min.",
        "totunitshealed": "Total units healed per min.",
        "dmgtoobj": "Damage to objects per min.",
        "timecc": "Time spent with crown control per min.",
        "totdmgtaken": "Total damage taken per min.",
        "magicdmgtaken": "Magic damage taken per min.",
        "physdmgtaken": "Physical damage taken per min.",
        "truedmgtaken": "True damage taken per min.",
        "goldearned": "Gold earned per min.",
        "goldspent": "Gold spent per min.",
        "totminionskilled": "Total minions killed per min.",
        "neutralminionskilled": "Neutral minions killed per min.",
        "ownjunglekills": "Own jungle kills per min.",
        "enemyjunglekills": "Enemy jungle kills per min.",
        "totcctimedealt": "Total crown control time dealt per min.",
        "pinksbought": "Pink wards bought per min.",
        "wardsbought": "Wards bought per min.",
        "wardsplaced": "Wards placed per min.",
        "turretkills": "# of turret kills",
        "inhibkills": "# of inhibitor kills",
        "dmgtoturrets": "Damage to turrets"
    }
    feature_names = [full_names.get(n, n) for n in X.columns]
    X.columns = feature_names
    return X, y
#print(allstats)


'''
Excised Jupyter Code:
# 
{
allstats = ml.get_main_frame()
X = allstats.drop(["win"], axis=1)
Y = allstats["win"]

OR

X, Y = ml.get_X_Y()
print(X, Y)
print(X["Gold earned per min."])
}

Xt, Xv, yt, yv = train_test_split(X,Y, test_size=0.2, random_state=10)
dt = xgb.DMatrix(Xt, label=yt.values)
dv = xgb.DMatrix(Xv, label=yv.values)

params = {
    "eta": 0.5,
    "max_depth": 4,
    "objective": "binary:logistic",
    "silent": 1,
    "base_score": np.mean(yt),
    "eval_metric": "logloss"
}
print(np.mean(yt))
model = xgb.train(params, dt, 3, [(dt, "train"), (dv, "valid")], early_stopping_rounds=5, verbose_eval=25)

shap.initjs()
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(Xv)
shap.force_plot(explainer.expected_value, shap_values[0,:], Xv.iloc[0,:])

#shap_values = explainer.shap_values(Xv.iloc[4425:4427], check_additivity=False)
shap.initjs()
explainer = shap.Explainer(model, X)
shap_values = explainer(X)
#shap_values = explainer.shap_values(Xv)
#shap.summary_plot(shap_values, Xv, max_display=5)
shap.plots.beeswarm(shap_values, max_display = 10)

explainer = shap.Explainer(model, X)
shap_values = explainer(X)
shap_values = explainer.shap_values(Xv.iloc[4425:4427], check_additivity=False)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(Xv)
top_inds = np.argsort(-np.sum(np.abs(shap_values), 0))

# make SHAP plots of the three most important features
for i in range(20):
    shap.dependence_plot(top_inds[i], shap_values, Xv)







'''
