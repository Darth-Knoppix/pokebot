import tweepy
from bot import *
from tweepy import api
from datetime import datetime
from PIL import Image, ImageFilter
import schedule
import time
import cred

last_id = 0
bot = None

def tweetBattle(message = ""):
    '''Send battle tweet'''
    #api.update_status("Images are incoming...")
    return api.update_with_media('scene.png', message)

def tweetVote(message="Choose a pokemon to battle!"):
    '''Ask users which pokemon to choose'''
    return api.update_status(message)

def collectTweets(tag = 'balbasaur'):
    '''Collect tweets based on hashtag'''
    return tweepy.Cursor(api.search, q='#' + tag, lang='en')

def collectVote():
    '''Get mentions recieved today'''
    return tweepy.Cursor(api.mentions_timeline, lang='en', since_id=today())

def printTweets(tweets):
    '''Print collection of tweets'''
    for tweet in tweets:
        print(tweet.text.encode('ascii', 'ignore'))

def composeTweet():
    '''Setup the battle image'''
    global bot
    bot = Bot()
    bot.preload()
    return bot.setup()

def today():
    '''Todays date in api readbale format'''
    return datetime.now().strftime('%Y-%m-%d')

def performBattle():
    '''Random battle'''
    global last_id
    message = composeTweet() + ', Who won?'
    tweet = tweetBattle(message)
    last_id = tweet.id
    print(message)

def announceWinner():
    '''Announce winner via tweet based on hashtags'''
    #api.update_status(message)
    myPokemonTweets = collectTweets(bot.myPokemon['name'])
    competitorPokemonTweets = collectTweets(bot.competitor['name'])
    
    myPokemonCount = 0
    for myTweet in myPokemonTweets.items():
        myPokemonCount += 1
    
    competitorPokemonCount = 0
    for competitorTweet in competitorPokemonTweets.items():
        myPokemonCount += 1

    if(myPokemonCount > competitorPokemonCount):
        message = bot.myPokemon['name'] + " won the battle!"
        bot.myPokemon['frontImage'].save('profilepic.png')
    elif(myPokemonCount < competitorPokemonCount):
        message = bot.competitor['name'] + " won the battle!"
        bot.competitor['frontImage'].save('profilepic.png')
    else:
        message = bot.myPokemon['name'] + " winds by default, it was a tough match!"
        bot.myPokemon['frontImage'].save('profilepic.png')
    print(message)
    api.update_status(message)
    api.update_profile_image('profilepic.png')
    

print('Authenticating...')
### Setup Tweepy with credientials
auth = tweepy.OAuthHandler(cred.CONSUMER_KEY, cred.CONSUMER_SECRET)
auth.set_access_token(cred.ACCESS_KEY, cred.ACCESS_SECRET)
api = tweepy.API(auth)

#performBattle()
#announceWinner()

print('Starting schedule')
schedule.every(30).seconds.do(performBattle)
schedule.every(1).minute.do(announceWinner)

while True:
    schedule.run_pending()
    time.sleep(1)

#voteTweet = tweetVote('Lets choose another one...')
#print(voteTweet.id)
#print(api.get_status('790672683155337217'))
#tweet(composeTweet())

#myPokemon, competitor = composeTweet()

#printTweets(collectTweets(myPokemon['name']))


#printTweets(collectTweets())



#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print(tweet.text)