import requests
import json
import datetime
import os
import MySQLdb
import MySQLdb.cursors
from StringIO import StringIO




lottoget = requests.get("""https://www.njlottery.com/api/v1/instant-games/games/?size=1000&_=1525504212758""")
resp = lottoget.json()

for items in resp:
    if items == 'games':
        gamelist = resp[items]
gamedict = dict()

for games in gamelist:
    gamedict[games['gameId']] = games

activegames = dict()

for games in gamedict:
    if gamedict[games]['validationStatus'] == 'ACTIVE':
        activegames[gamedict[games]['gameId']] = gamedict[games]

# algorithms for win percent

# activegames keys are the current active NJ Lotto instant games
# each game contains a dictionary with the following keys

#       ticketPrice	gameId	totalTicketsPrinted	gameName	prizeTiers	disableDate	endDistributionDate
#       launchDate	validationStatus	startDistributionDate
#
# prizeTiers contains a list of dictionaries, there is no set length.
# prizeTiers dictionaries has the following keys

#       claimedTickets	paidTickets	tierNumber	winningTickets	originalTierNumber	tierType	prizeDescription	prizeAmount

################################################

# to figure out the chance to win a prize:
#
# add together winningTickets from prizeTiers (referred to as totalWin)
# divide totalTicketsPrinted by totalWin (referred to as winRatio)

################################################

################################################

# to estimate how many tickets have been bought:
#
# add together paidTickets from prizeTiers (referred to as totalPaid)
# multiply winRatio with totalPaid (result referred to as remainingPrintedTickets or rpt)

################################################

################################################

# to estimate current chances at remaining tickets:
#
# add paidTickets together (tpt), add winningTickets together (twt)
# twt - tpt  = (rwt) || totalwinningTickets - totalpaidTickets = remainingwinningTickets
# rpt / rwt = (cwr) divide remainingprintedTickets by remainingwinningTickets = currentwinRatio 
#

################################################
######### Big Money Spectacular gameId #########
################################################

# 1460
# 1462
# 1393
# 1419
# 1433

# *************************************************
# *************************************************
#
######## SQL select/insert/update
#
#

class sqllotto:
    
    def __init__(self, data, mode):
        self.connecter = MySQLdb.connect(user='root', passwd='', db='lotto', cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.connecter.cursor()
        self.data = data
        self.mode = mode
        
    def updatedb(self):
        cursor.execute("""select * from `current_games` order by `id` desc""")
        cursor.execute("""INSERT INTO `current_games`(`gameId`, `gameName`) VALUES (%s,%s)""", (activegames['1420']['gameId'], activegames['1420']['gameName']))
        cursor.execute("""INSERT INTO `current_games`(`gameId`, `gameName`) VALUES (%s,%s)""", (activegames['1420']['gameId'], activegames['1420']['gameName']))
        
connector = MySQLdb.connect(user='root', passwd='', db='lotto', cursorclass=MySQLdb.cursors.DictCursor)
cursor = connector.cursor()

for games in activegames:
        cursor.execute("""INSERT INTO `current_games` (`gameId`, `gameName`, `ticketPrice`, `totalTicketsPrinted`, `launchDate`, `disableDate`) VALUES (%s,%s,%s,%s,%s,%s)""", (activegames[games]['gameId'], activegames[games]['gameName'], activegames[games]['ticketPrice'], activegames[games]['totalTicketsPrinted'], activegames[games]['launchDate'], activegames[games]['disableDate']))

for games in activegames:
        for prizes in activegames[games]['prizeTiers']:
            cursor.execute("""INSERT INTO `game_prizes`(`gameId`,`paidTickets`,`winningTickets`,`prizeDescription`,`tierNumber`) VALUES (%s,%s,%s,%s,%s)""", (activegames[games]['gameId'], prizes['paidTickets'], prizes['winningTickets'], prizes['prizeDescription'], prizes['tierNumber']))

########### GET IMAGES ###########

    
    
def getImage(url, name, folder='./'):
    file = '{}{}'.format(folder, name)
    with open(name, 'wb') as f:
        r = requests.get(url, stream=True)
        for block in r.iter_content(1024):
            if not block:
                break
            f.write(block)


for games in activegames:
    gameid = games    
    imgURL = '''https://www.njlottery.com/content/dam/portal/images/instant-games/0''' + gameid + '''/thumb-rc@2X.png'''
    filename = str(games) + '''.png'''
    getImage(imgURL, filename)
    
    
    

