#Sprites taken from http:#www.spriters-resource.com/game_boy_advance/pokemonfireredleafgreen/sheet/3866/
#UI taken form http://www.spriters-resource.com/game_boy_advance/pokemonfireredleafgreen/sheet/33690/
#New Sprites come form http://floatzel.net/
#Getting stats from https://github.com/stefankendall/pokemondatacollector

from PIL import Image, ImageFilter
import urllib
import json
import simplejson
import random
import sys
import math


class Bot():

    def __init__(self):
        self.url          = 'pokemon.json'
        self.weatherUrl   = 'http://api.openweathermap.org/data/2.5/weather?id=2179538&APPID=6724a4ca93cbb79b23fc5e6243d867dc&units=metric'
        self.statsUrl     = 'https://raw.githubusercontent.com/stefankendall/pokemondatacollector/master/base_stats.json'
        self.stageSheet   = Image.open('battleBG_sheet.png')
        self.UI           = Image.open('battleUI.png')
        self.basicData    = {}
        self.statsData    = {}
        self.weatherData  = {}
        self.pokemon      = {}
        self.temperatures = []
        self.pokemonCount = 0
        self.competitor   = None
        self.myPokemon    = None
        self.have_drawn   = False
        self.stage        = None
        self.dSpriteWidth = 96
        self.stage        = None
        self.scene        = Image.new('RGB', (220, 110), (255,255,255))

    #Select stage based on current weather
    def selectStage(self):
        if len(self.weatherData['weather']) < 1:
            return 'grass'
    
        state = self.weatherData['weather'][0]['id']
        out = ''
        if state >= 200:
            out = 'dragon'
        if state >= 300:
            if(random.random() > 0.5):
                out = 'grass'
            else:
                out = 'bug'
        if state >= 500:
            out = 'water'
        if state >= 600:
            out = 'ice'
        if state >= 700:
            if random() > 0.5:
                out = 'ghost'
            else:
                out = 'poison'
        if state >= 800:
            out = 'earth'
        if state >= 900:
            out = 'steel'
        return out
        

    # Check if number
    def isNumber(self, n):
        return not isNaN(parseFloat(n))


    # Clean the name and remove non ascii characters
    def cleanName(self, name):
        return name.lower().replace(' ', '-').replace('♀', '-f').replace('♂', '-m').replace('.', '').replace("'", '')

    # Draw string as pokemon font
    def type(self, sentence, location):
        sentence = str(sentence).upper()
        letter = ''
        row = 124
        posStart = 171;       # Letters start here (X)
        charImage = {'width': 5, 'padding': 2}
        letterXPos = 0
        halfAlphaOffset = 0
        pos = 0

        for letter in sentence:
            # Check if past J, change offset
            if ord(letter) >= 74:
                halfAlphaOffset = 2
            else:
                halfAlphaOffset = 0

            #Is a letter or number
            if letter.isdigit():
                row = 159
                letterXPos = posStart + ((int(letter)) * (charImage['width'] + charImage['padding']))
            else:
                letterXPos = posStart + ((ord(letter) - 65) *  (charImage['width'] + charImage['padding'])) - halfAlphaOffset
            
            UIImage = self.UI.crop((letterXPos, row, letterXPos + charImage['width'], row + 8))
            self.scene.paste(UIImage, (location['x'] + (pos * charImage['width']), location['y']), UIImage)
            pos += 1

    # Give pokemon stats
    def setupPokemon(self, pokemon):
        handicap = 1
        pokemon['stats'] = {}
        # Get and calc relevant stats
        pokemon['stats']['maxHealth'] = self.statsData[pokemon['name'].replace('.', '')]['hp']

        #Set health based on type of pokemon
        temp = self.weatherData['main']

        if len(self.weatherData['weather']) < 1:
            temp = 25
        
        handicap = random.random()

        pokemon['stats']['health']    = pokemon['stats']['maxHealth'] - (handicap * pokemon['stats']['maxHealth'])
        pokemon['stats']['level']     = random.randint(1, 100)

    # Choose a pokemon
    def choosePokemon(self, type):
        choice = 1

        if(type is 'RANDOM'):
            choice = random.randint(1, self.pokemonCount)
        
        choice = str(choice)
        return self.pokemon[choice]

    def getSprite(self, id, type):
        seperator = '/'
        if type is 'normal':
            seperator = ''
            type = ''

        #Construct the url to retrieve sprite from web
        url = 'http://floatzel.net/pokemon/black-white/sprites/images/' + type + seperator + id + '.png'
        return Image.open(urllib.request.urlopen(url))

    def drawStage(self, name):
        offset = 0
        stageWidth = 240
        # Choose location of stage depending on type
        if(name is 'normal'):
            offset = 0
        elif(name is 'grass'):
            offset = stageWidth * -1
        elif(name is 'ice'):
            offset = stageWidth * -2
        elif(name is 'earth'):
            offset = stageWidth * -3
        elif(name is 'water'):
            offset = stageWidth * -4
        elif(name is 'steel'):
            offset = stageWidth * -5
        elif(name is 'dragon'):
            offset = stageWidth * -6
        elif(name is 'poison'):
            offset = stageWidth * -7
        elif(name is 'bug'):
            offset = stageWidth * -8
        elif(name is 'ghost'):
            offset = stageWidth * -9
    
        self.scene.paste(self.stageSheet, (offset,0))

    def drawBattleUI(self):
        healthUI = self.UI.convert('RGBA')
        theirStatusBar = {'x': 50, 'y': 5, 'width': 100, 'height': 29}

        def drawHealthBar(health, maxHealth, position):
            healthPercentage = health/maxHealth
            healthBar = healthPercentage * position['width']

            #Draw backing of health bar
            healthUIImage = healthUI.crop((118, 21, 1,3))
            self.scene.paste(healthUIImage, (position['x'], position['y']), healthUIImage)

            #Draw actual health
            if(healthPercentage < 0.75):
                healthUIImage = healthUI.crop((117, 13, 1, 3))
                self.scene.paste(healthUIImage, (position['x'], position['y']), healthUIImage)
            if healthPercentage < 0.25:
                healthUIImage = healthUI.crop((117, 13, 1, 3))
                self.scene.paste(healthUIImage, (position['x'], position['y']), healthUIImage)
            else:
                healthUIImage = healthUI.crop((117, 9, 1, 3))
                self.scene.paste(healthUIImage, (position['x'], position['y']), healthUIImage)

        # Draw competitior UI
        # Competitor Status BG
        UIImage = self.UI.crop(
                        (
                            0,
                            0,
                            100,
                            29
                        )
                    )
        self.scene.paste(UIImage, (theirStatusBar['x'],theirStatusBar['y']), UIImage)

        # Competitor Health
        drawHealthBar(
            self.competitor['stats']['health'],
            self.competitor['stats']['maxHealth'],
            {'x': 39 + theirStatusBar['x'], 'y': 17 + theirStatusBar['y'], 'width': 48, 'height': 3}
        )

        # Competitor Level
        self.type(self.competitor['stats']['level'], {'x': theirStatusBar['x'] + 83, 'y': theirStatusBar['y'] + 8})

        # Competitor Name
        self.type(self.competitor['name'], {'x': theirStatusBar['x'] + 7, 'y': theirStatusBar['y'] + 8})

    def preload(self):
        self.basicData    = simplejson.loads(open(self.url, encoding='utf8').read())
        self.statsData    = simplejson.load(urllib.request.urlopen(self.statsUrl))
        self.weatherData  = simplejson.load(urllib.request.urlopen(self.weatherUrl))


    def setup(self):
        self.selectStage()
        self.basicData = self.basicData['pokemon']

        item = 0
        while item < 151:
            self.pokemon[self.basicData[item]['id']] = self.basicData[item]
            self.pokemonCount += 1
            item += 1

        # Setup pokemon
        # Choose pokemon
        self.competitor  = self.choosePokemon('RANDOM')
        self.myPokemon   = self.choosePokemon('RANDOM')

        # Get backgrounds
        self.myPokemon['backImage']    = self.getSprite(self.myPokemon['id'], 'back')
        self.myPokemon['frontImage']    = self.getSprite(self.myPokemon['id'], 'normal')
        self.competitor['frontImage']  = self.getSprite(self.competitor['id'], 'normal')

        self.setupPokemon(self.competitor)

        # Set offset to place on the canvas correctly
        self.myPokemon['x_offset']   = -32 + self.dSpriteWidth/2
        self.myPokemon['y_offset']   = -12 + self.dSpriteWidth/2
        self.competitor['x_offset']  = 140
        self.competitor['y_offset']  = 0

        # Draw main elements
        self.drawStage(self.stage)
        #Draw my Pokemon
        myPokemonImage = self.myPokemon['backImage'].convert('RGBA')
        self.scene.paste(myPokemonImage, (int(self.myPokemon['x_offset']), int(self.myPokemon['y_offset'])), myPokemonImage)
        # Draw UI
        self.drawBattleUI()

        #Draw the competitor
        myCompetitorImage = self.competitor['frontImage'].convert('RGBA')
        self.scene.paste(myCompetitorImage, (self.competitor['x_offset'], self.competitor['y_offset']), myCompetitorImage)
        message = self.myPokemon['name'] + ' VS ' + self.competitor['name']
        output = self.scene.resize((440, 220), Image.ANTIALIAS)
        output.save('scene.png')
        return message
