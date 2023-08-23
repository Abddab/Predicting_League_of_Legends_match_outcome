# Attempt to predict the outcome of a League of Legends match (In Progress)
The goals of this project are to:
1. Understand which pieces of information (features) have the greatest impact (feature importance) on the win/loss of a League of Legends game :dart:
2. Attempt to predict the outcome of a League of Legends game using the data pulled from Riot Games's API :dart:

Before we begin, what exactly is League of Legends? League of Legends (or LoL) is a team-based strategy game where two teams of five powerful champions face off to destroy the other's Nexus. You can choose from over 140 different champions to make epic plays, secure kills, and take down towers as you battle your way to victory ([League of Legends](https://www.leagueoflegends.com/en-us/how-to-play/), n.d)

There's an insane amount of information generated in every single one of the hundreds of millions of games played every single month around the world. Thankfully, Riot Games (the game developer) gives us access to all this data through their **[API](https://developer.riotgames.com/)**.
## The Process
<p align="center">
  <img src="https://user-images.githubusercontent.com/56210553/197674782-91d23cc1-7432-42fe-9dc3-552891fce3ea.png" width="600"/>
</p>

**(Image from [sudeep.co](https://www.sudeep.co/data-science/2018/02/09/Understanding-the-Data-Science-Lifecycle.html))**

This is the complete cycle we'll go through to reach the goals of the project, so let's start!
### Step 1: Understanding the problem we are trying to solve
To understand a problem, one should ask relevant questions. And to ask relevant questions, one should first understand the "domain" in which the problem exists. It would obviously be very hard for someone to create an effective model if they never player a game of League of Legends in their life. You have to experience the game by yourself to understand the factors that can play an important role in the win/loss of a game.

If you take a look at Riot Games's API, there's literally hundreds of different features that could be used to train a predictive model. So the question is: which ones are the most important and the most likely to influence the result of a game? This question is probably impossible to answer without studying every single feature that Riot Games gives us access to, but an experienced player can make an educated guess based on his personal game experience.

Here's some data I think would be interesting to track based on my experience playing League of Legends:

* Check if a player WAS in a 'tilted' state (Lost the past 2 games in a row). Sum the number of players in each team that are in 'tilted' state. Compare and observe correlation with winning/losing the next game.
* Check if a player WAS in 'confident' state (Won the 2 past games in a row). Sum the number of players in each team that are in 'confident' state. Compare and observe correlation with winning/losing the next game.
* Compute the average KDA (of the last 5 games) of each player on the team and label them as 'Feeders', 'Carries' or 'Neutral'. Compare the labels on each team and 
* Look up the global winrates of the champions played by each player. Compare the averages of the winrates and observe if a higher 'quality' pool of champions correlates with the win of the game.
* Compare the average vision scores of each team (**Maybe**).
* Check if a team has a jungler that performed well in the past.
* Check the mastery level of the champion played by the players. Does a higher number of 'masters' on a team correlate with higher chance of winning?
* Check the **champion** winrate of each player.
* Check the **total** winrate of each player and categorize them as 'smurfs' or not.




The impact of all these features will be measured further in the process.


### Step 2: Gathering the necessary data

Link to the Python Script: 
https://github.com/Abddab/Predicting_League_of_Legends_match_outcome/blob/main/data_collection.py

The script has been written to extract data from the Riot Games’s API. Since the Riot Games API has a rate limit of 100 API Calls per 2 minutes, a snippet of code has been built into the script to wait for the rate limit to expire before continuing the execution of the code. 

<p align="center">
  <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/56210553/262516674-8666c161-5839-4c85-8ad0-8a45f74f7e0a.png" width="600"/>
</p>




 
Below is a sample of the data I have decided to extract. This raw data will be useful to engineer the features that will go into training the predictive model.
 

Considering the rate limit imposed by Riot Games, the script will have to run multiple hours (if not days) to extract an amount of data that is suitable for the training of a predictive model. 
