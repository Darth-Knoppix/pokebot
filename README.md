#PS3 MDDN 342 2016

-----
### Idea
-----

My idea is to use the pokemon data from corpora (https://github.com/dariusk/corpora/blob/master/data/games/pokemon.json).
I saw this and thought it could be interesting to show a battle between two pokemon
like in the games however it would be through the twitter bot.

I have some basic image loading working and random pokemon being selected.

I would like to eventually have a complete system where a battle can occur over
the course of a few posts. Some stretch goals include pokemon selection by poll
through twitter and eventually supporting a 'campaign' where the pokemon levels up.

This can get very complex very quickly but I am interested to see how people respond
to this idea and I want to see how far I can push it.

The artifact is a image of a typical battle screen in the Pokemon games, the properties
are as follows:
- Enemy Pokemon/Competitor
  - Health
  - Level
- Player Pokemon

The Pokemon will be randomly selected along with some basic stats i.e. level and health.
The stage and level will be determined by weather data. I would like to adjust the level
based on the number of #pokemon_name, found on twitter however the API is not powerful enough.
By adding weather data, It allows for greater variation however I would have liked to add more
relevant data through twitter or a more user interactable medium.

### Refinement
To refine my bot I wanted to add some more interactivity. To do this I rewrote my code in python
so I could reduce the distance betwee getting information from twitter and drawing the sketch.

This allowed me to have some more direct interaction between twitter itself and my pokemon battle.
The bot will run to aschedule and pick a random battle. The scene will be dertermined as before by 
weather data and will gather the information for the Pokemon form various internet sources.
It will assk 'Who won?" promting the user for some input, this will take the form of a tweet with the hashtag
of one of the pokemon, the more tweets with that particular hashtag will win the battle. The bot will
retrieve the tweets from the last day to sum.

A challenge was getting the correct data form Twitter and figuring out a way to use it effectively.
 


The bot is online at https://twitter.com/poke_battle_bot