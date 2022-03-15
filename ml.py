import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as pl

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
# print(stats)

# merge into a single DataFrame
a = pd.merge(participants, matches, left_on="matchid", right_on="id")
allstats_orig = pd.merge(a, stats, left_on="matchid", right_on="id")
allstats = allstats_orig.copy()

# drop games that lasted less than 10 minutes
allstats = allstats.loc[allstats["duration"] >= 10*60,:]
# print(allstats)



