import requests
import json
import datetime
import os
import pyodbc
from io import StringIO
from datetime import datetime as dt

class lotto_info:
	
	def __init__(self, state='NJ'):
		self.state = state
		self.today_epoc = str(dt.today().timestamp()).split('.')[0]
		self.url_dict = {'NJ':f"""https://www.njlottery.com/api/v1/instant-games/games/?size=1000&_={self.today_epoc}"""}
		self.dl = pyodbc.drivers()
		self.sql_params = {'driver':self.dl[-2], 'user':'root', 'password':'', 'server':'localhost', 'port':'3306', 'db':'lotto'}
		sp = self.sql_params
		self.driver = pyodbc.connect(f'''DRIVER={sp['driver']};SERVER={sp['server']};PORT={sp['port']};DATABASE={sp['db']};UID={sp['user']};PWD={sp['password']}''')
		self.cursor = self.driver.cursor()
		self.gamedict = {}
		
		
	def check_tbl(self):
		c = self.cursor
		game_cols = ['game_id', 'game_name', 'validation_status', 'ticket_price', 'launch_date', 'start_distribution_date', 'end_distribution_date', 'disable_date', 'prize_tiers', 'total_tickets_printed']
		odds_cols = ['total_tickets_printed', 'total_winning_tickets', 'total_paid_tickets', 'winning_percent', 'winning_ratio', 'percent_winning_claimed', 'estimated_tickets_remaining', 'estimated_remaining_wins', 'estimated_remaining_winning_percent', 'estimated_remaining_winning_ratio']
		prize_tier_cols = ['winning_tickets', 'paid_tickets', 'percent_of_winners', 'percent_winners_paid', 'remaining_winning_tickets', 'remaining_winning_percent', 'remiaining_winning_ratio', 'prize_amount']
		col_str = str(' varchar(255), ').join(game_cols) + ' varchar(255)'
		odds_str = str(' varchar(255), ').join(odds_cols) + ' varchar(255)'
		pt_str = str(' varchar(255), ').join(prize_tier_cols) + ' varchar(255)'
		tbls = c.tables().fetchall()
		if len(tbls) != 0:
			if 'active_games' in tbls[0]:
				tbl_exists = True
			else:
				tbl_exists = False
		else:
			tbl_exists = False
			
		if tbl_exists == False:
			print('active_games Table not in DB, creating...')	
			create_tbl_sql = str(f'''CREATE TABLE active_games ({col_str});''')
			c.execute(create_tbl_sql)
		tbls = c.tables().fetchall()
		print(tbls)
		# return create_tbl_sql
		
			
	
	def request_info(self, state):
		
		req_url = self.url_dict[state]
		
		req = requests.get(req_url)
		resp = req.json()
		gl =  resp['games']
	
		gamedict = {g['gameId']:g for g in gl if g['validationStatus'] == 'ACTIVE'}
		for g in gamedict:
			ld = int(str(gamedict[g]['launchDate'])[:-3])
			dd = int(str(gamedict[g]['disableDate'])[:-3])
			gamedict[g]['launchDate'] = dt.date(dt.fromtimestamp(ld)).isoformat()
			gamedict[g]['disableDate'] = dt.date(dt.fromtimestamp(dd)).isoformat()
		self.gamedict = gamedict
		return gamedict
	
	def game_odds(self, gameid):
		
		if len(self.gamedict) < 1:
			return False
		game_odds = {}
		
		cg = self.gamedict[gameid]
		cgpt = cg['prizeTiers']
		cg_ttp = cg['totalTicketsPrinted']
		cg_twt = 0
		cg_tpt = 0
		
		for pt in cgpt:
			cg_twt += pt['winningTickets']
			cg_tpt += pt['paidTickets']
		cg_wp = cg_twt/cg_ttp*100
		cg_wr = cg_ttp/cg_twt
		cg_pwc = cg_tpt/cg_twt * 100
		cg_ert = cg_ttp - (cg_wr*cg_tpt)
		cg_erw = cg_twt - cg_tpt
		cg_erwp = cg_ert/cg_erw * 100
		cg_erwr = cg_ert/cg_erw
		game_odds = {'total_tickets_printed':cg_ttp, 'total_winning_tickets':cg_twt, \
					 'total_paid_tickets':cg_tpt, 'winning_percent':cg_wp, 'winning_ratio':cg_wr, \
					 'percent_winning_claimed':cg_pwc, 'estimated_tickets_remaining':cg_ert, \
					 'estimated_remaining_wins':cg_erw, 'estimated_remaining_winning_percent':cg_erwp, \
					 'estimated_remaining_winning_ratio':cg_erwr,'odds':{}}
		ptodds= {}
		for pt in cgpt:
			pt_wt = pt['winningTickets']
			pt_pt = pt['paidTickets']
			if pt_pt != 0:
				pt_wp = pt_wt/cg_ttp * 100
				pt_wr = cg_ttp/pt_wt
			else:
				pt_wp = 0
				pt_wr = 0
				
			pt_pow = pt_wt/cg_twt * 100
			pt_rwt = pt_wt - pt_pt
			if pt_rwt !=0:
				pt_erwp = pt_rwt/cg_ert * 100
				pt_erwr = cg_ert/pt_rwt
			else:
				pt_erwp = 0
				pt_erwr = 0
			pt_pa = str('$') + str(pt['prizeAmount'])[:-2] + str('.00')
			if pt_pt == '0' or pt_pt == 0:
				pt_ptc = 0
			else:	
				pt_ptc = pt_pt/pt_wt * 100
			pt_tn = pt['tierNumber']
			if pt_tn not in ptodds:
				ptodds[pt_tn] = {'winning_tickets':pt_wt, 'paid_tickets':pt_pt, 'percent_of_winners':pt_pow, 'percent_winners_paid':pt_ptc, 'winning_percent':pt_wp, 'winning_ratio':pt_wr, 'remaining_winning_tickets':pt_rwt, 'remaining_winning_percent':pt_erwp, 'remiaining_winning_ratio':pt_erwr, 'prize_amount':pt_pa}
				
				
		
		return game_odds, ptodds
			
			
			
		
		
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
# 
# class sqllotto:
#     
#     def __init__(self, data, mode):
#         self.connecter = MySQLdb.connect(user='root', passwd='', db='lotto', cursorclass=MySQLdb.cursors.DictCursor)
#         self.cursor = self.connecter.cursor()
#         self.data = data
#         self.mode = mode
#         
#     def updatedb(self):
#         cursor.execute("""select * from `current_games` order by `id` desc""")
#         cursor.execute("""INSERT INTO `current_games`(`gameId`, `gameName`) VALUES (%s,%s)""", (activegames['1420']['gameId'], activegames['1420']['gameName']))
#         cursor.execute("""INSERT INTO `current_games`(`gameId`, `gameName`) VALUES (%s,%s)""", (activegames['1420']['gameId'], activegames['1420']['gameName']))
#         
# connector = MySQLdb.connect(user='root', passwd='', db='lotto', cursorclass=MySQLdb.cursors.DictCursor)
# cursor = connector.cursor()
# 
# for games in activegames:
#         cursor.execute("""INSERT INTO `current_games` (`gameId`, `gameName`, `ticketPrice`, `totalTicketsPrinted`, `launchDate`, `disableDate`) VALUES (%s,%s,%s,%s,%s,%s)""", (activegames[games]['gameId'], activegames[games]['gameName'], activegames[games]['ticketPrice'], activegames[games]['totalTicketsPrinted'], activegames[games]['launchDate'], activegames[games]['disableDate']))
# 
# for games in activegames:
#         for prizes in activegames[games]['prizeTiers']:
#             cursor.execute("""INSERT INTO `game_prizes`(`gameId`,`paidTickets`,`winningTickets`,`prizeDescription`,`tierNumber`) VALUES (%s,%s,%s,%s,%s)""", (activegames[games]['gameId'], prizes['paidTickets'], prizes['winningTickets'], prizes['prizeDescription'], prizes['tierNumber']))
# 
# ########### GET IMAGES ###########
# 
#     
#     
# def getImage(url, name, folder='./'):
#     file = '{}{}'.format(folder, name)
#     with open(name, 'wb') as f:
#         r = requests.get(url, stream=True)
#         for block in r.iter_content(1024):
#             if not block:
#                 break
#             f.write(block)
# 
# 
# for games in activegames:
#     gameid = games    
#     imgURL = '''https://www.njlottery.com/content/dam/portal/images/instant-games/0''' + gameid + '''/thumb-rc@2X.png'''
#     filename = str(games) + '''.png'''
#     getImage(imgURL, filename)
#     
    
    

