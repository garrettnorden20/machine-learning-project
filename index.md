# Predicting the Winner of a Match based on Match Data in League of Legends


### Introduction

League of Legends is a multiplayer online battle arena video game created by Riot Games. Matches are 5v5, where two teams attempt to take the other team's side of the map while defending their own. It is considered the world's largest esport, with millions of unique viewers each month for tournaments. 

### Problem Definition

Our goal is to forecast the winner of a match given all the data in the match (such as the characters on each team, damage done per minute, etc). There are many ways this model could be used. Teams wanting to experiment with new team compositions without wanting to hurt their rankings could see how changes in heroes could affect their predicted win rate. Players could also see the most important elements of a match - i.e., the features that drive the prediction the most. Many of the viewers of competitive matches could also use these predictions to make more informed betting decisions. 

### Data
The dataset this model uses was pulled from Riot Games' API and consists of over 180,000 individual matches from 2014-2018, and was downloaded from here.
https://www.kaggle.com/paololol/league-of-legends-ranked-matches

Each match has 80 features and a label of which team won the match.

### Method: Supervised Learning
Task: Predict the winner of the match based off the features of the match

Train/Test Data: Match data taken from Riot Games' API, with a label of which team won

Output: Predict which team will win the match by giving a percentage chance, based on the match data

Methods: Basic neural net, decision tree, random forest, dimensional reduction

### Potential Results and Discussion
Build a classifier that will accurately determine the outcome of a match with accuracy based on the given parts of a match:

Greater than 95% accuracy in predicting the winner when given all features of match data (particularly data that occurs during the match, such as total damage dealt and taken) 

Greater than 75% accuracy in predicting the winner when only given features of match data that would be known before the match (such a character selection, region, etc)

### Proposed Timeline 

|               Week               |                                         Work                                         | Noah       | Garrett    | Benjamin   | Zhenyu     | Jiacheng   |
|:--------------------------------:|:------------------------------------------------------------------------------------:|------------|------------|------------|------------|------------|
| 2/20/22 (Proposal Due)           | Finish proposal and video, gather data                                               | code       | code       | research   | code       | research   |
| 2/27/22                          | Setup repository and Python files, determine which dependecies to use, sanitize data | research   | code       | code       | research   | code       |
| 3/6/22                           | Analyze data and research neural network and random forest                           | code       | research   | code       | research   | code       |
| 3/13/22                          | Analyze data and continue research, begin groundwork implementation                  | research   | code       | research   | code       | test model |
| 3/20/22                          | Implement the neural networks and random forest                                      | test model | code       | code       | research   | code       |
| 3/27/22                          | Continue implementation, begin to work on midpoint report                            | video      | code       | video      | code       | code       |
| 4/3/22 (Project midpoint report) | Complete minimum viable product, create midpoint report                              | code       | test model | code       | test model | code       |
| 4/10/22                          | Wrap up final product, work on stretch goals                                         | code       | code       | test model | test model | code       |
| 4/17/22                          | Work on stretch goals, create final report                                           | code       | test model | code       | code       | code       |
| 4/24/22 (Final Project Due)      | Finish final report, create video                                                    | video      | code       | video      | code       | test model |

### Video Presentation
https://drive.google.com/file/d/1q2MiASSYoRDk6oPbt-X9nTPIFel2G4xx/view?usp=sharing

### References
Pei, Annie. “This Esports Giant Draws in More Viewers than the Super Bowl, and It's Expected to Get Even Bigger.” CNBC, CNBC, 14 Apr. 2019, https://www.cnbc.com/2019/04/14/league-of-legends-gets-more-viewers-than-super-bowlwhats-coming-next.html. 

Cabrol, Dan. “Predicting Outcome of League of Legend Ranked Games in Champselect via Machine Learning.” Medium, Medium, 9 Nov. 2020, https://ffaheroes.medium.com/predicting-outcome-of-league-of-legend-ranked-games-in-champselect-via-machine-learning-8f9d86669eae. 

Do, Tiffany D., et al. “Using Machine Learning to Predict Game Outcomes Based on Player-Champion Experience in League of Legends.” The 16th International Conference on the Foundations of Digital Games (FDG) 2021, 2021, https://doi.org/10.1145/3472538.3472579.

Kim, Seouk Jun. “Match Prediction in League of Legends Using Vanilla Deep Neural Network.” Medium, Towards Data Science, 18 Apr. 2020, https://towardsdatascience.com/match-prediction-in-league-of-legends-using-vanilla-deep-neural-network-7cadc6fce7dd. 

