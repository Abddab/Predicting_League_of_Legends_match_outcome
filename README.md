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

Here's some data I think would be interesting to track based on my experience playing League of Legends.
Let's divide by team data and current game data.
* Check if a player is in 'tilted' state (Lost 2 games in a row). Observe correlation with winning/losing the next game.
* Check if a player is in 'confident' state (Won 2 games in a row). Observe correlation with winning/losing the next game.
* Compute the KDA of each player on the team and label them as 'Feeders', 'Carries' or 'Neutral'.
* Look up the global winrates of the champions played by each player. Compare the averages of the winrates and observe if a higher 'quality' of champions correlates with the win of the game.

**To include in the future since it requires additional data (takes a very long time to pull data from the API at the rate allowed of 100 requests per 2 minutes):**
* Compute the average KDA (kill/death/assist) ratio of the last 5 games played by each member of the teams. Label them as 'Feeders' or 'Carries' or 'Neutral' based on their KDA. Observe the correlation between the number of feeders/carries on a team and the win/loss.
* Sum the total number of 'tilted'/'confident' players in a team. Compare the two teams.
* Check the mastery level of the champion played by the players. Does a higher number of 'masters' correlate with higher chance of winning?


The impact of all these features will be measured further in the process.


