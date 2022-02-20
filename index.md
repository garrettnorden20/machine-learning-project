# Predicting Ranking Based on Other Player Data in League of Legends


### Introduction

League of Legends is a multiplayer online battle arena video game created by Riot Games. Matches are 5v5, where two teams attempt to take the other team's side of the map while defending their own. It is considered the world's largest esport, with millions of unique viewers each month for tournaments. 

### Problem Definition

Our goal is to forecast the winner of a match given all the data in the match (such as the characters on each team, damage done per minute, etc). There are many ways this model could be used. Teams wanting to experiment with new team compositions without wanting to hurt their rankings could see how changes in heroes could affect their predicted win rate. Players could also see the most important elements of a match - i.e., the features that drive the prediction the most. Many of the viewers of competetive matches could also use these predictions to make more informed betting decisions. 

### Data
The dataset this model uses was pulled from Riot Games' API and consists of over 180,000 individual matches from 2014-2018, and was downloaded from here.
https://www.kaggle.com/paololol/league-of-legends-ranked-matches

Each match has 80 features and a label of which team won the match. 

### Method: Supervised Learning
Task: Predict the winner of the match based off the features of the match
Train/Test Data: Match data taken from Riot Games' API, with a label of which team won
Methods: Basic neural net, decision tree, random forest

