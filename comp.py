from bs4 import BeautifulSoup
import lxml
import matplotlib.pyplot as plt
import time
import csv
import sys
import datetime
import numpy as np
import time
from datetime import timedelta
import pandas as pd

match_list = []
updated_match_list = []

class Match:
	def __init__(self, map, time, wait_time, duration, viewer_count, ping, kills, assists, deaths, mvp_count, hsp, score, rounds_for, rounds_against):
		self.map = map
		self.time = time
		self.wait_time = wait_time
		self.duration = duration
		self.viewer_count = viewer_count
		self.ping = ping
		self.kills = int(kills)
		self.assists = int(assists)
		self.deaths = int(deaths)
		self.mvp_count = mvp_count
		self.hsp = int(hsp[:-1]) # Converts 37% to 37
		self.headshot_kills = self.get_headshot_kills()
		self.score = int(score)
		self.rounds_for = int(rounds_for)
		self.rounds_against = int(rounds_against)

	def get_headshot_kills(self):
		return round(self.kills * self.hsp/100)

	def __eq__(self, other):
		return self.__dict__ == other.__dict__
	
class Player:
	def __init__(self, name):
		self.name = name
		self.matches = []
	
	def add_match(self, match) -> None:
		self.matches.append(match)

	def get_all_maps(self) -> list:
		list_of_maps = []
		for match in self.matches:
			if match.map not in list_of_maps:
				list_of_maps.append(match.map)
		return list_of_maps

	def get_headshot_pct(self):
		headshot_kills = 0
		for match in self.matches:
			headshot_kills+=match.get_headshot_kills()
		return round(headshot_kills/self.get_kills(), 3)

	def get_kills(self) -> int:
		kills = 0
		for match in self.matches:
			kills+=match.kills
		return kills
	def get_deaths(self) -> int:
		deaths = 0
		for match in self.matches:
			deaths+=match.deaths
		return deaths

def num_wins():
	counter = 0
	for match in updated_match_list:
		if(int(match.rounds_for) > int(match.rounds_against)):
			counter = counter + 1
	return counter

def num_losses():
	counter = 0
	for match in updated_match_list:
		if(int(match.rounds_for) < int(match.rounds_against)):
			counter = counter + 1
	return counter

def num_ties():
	counter = 0
	for match in updated_match_list:
		if(int(match.rounds_for) == int(match.rounds_against)):
			counter = counter + 1
	return counter

####################################################################
#  Plots map win/loss/tie percentages as a bar graph               #
#   															   #
####################################################################
def plot_map_win_pct(map_stats):
	barWidth = 0.25
	fig = plt.subplots(figsize =(12, 8))
	win_list, loss_list, tie_list = [], [], []
	for mapName in map_stats:
		win_list.append(map_stats[mapName]["wins"]/map_stats[mapName]["total"])
		loss_list.append(map_stats[mapName]["losses"]/map_stats[mapName]["total"])
		tie_list.append(map_stats[mapName]["ties"]/map_stats[mapName]["total"])

	br1 = np.arange(len(win_list))
	br2 = [x + barWidth for x in br1]
	br3 = [x + barWidth for x in br2]
	plt.bar(br1, win_list, color="g", width=barWidth, label="Wins")
	plt.bar(br2, loss_list, color="r",width=barWidth, label="Losses")
	plt.bar(br3, tie_list, color="y", width=barWidth, label="Ties")
	plt.xlabel('Map', fontweight ='bold', fontsize = 15)
	plt.ylabel('Percentage', fontweight ='bold', fontsize = 15)
	plt.xticks([r + barWidth for r in range(len(win_list))],
        map_stats.keys())
	plt.legend()
	plt.show()

####################################################################
#  Plots map KDA values as a bar graph                             #
#   															   #
####################################################################
def plot_map_kda_stats(map_performance_stats):
	barWidth = 0.25
	fig = plt.subplots(figsize =(12, 8))
	kill_list, death_list, assist_list = [], [], []
	for mapName in map_performance_stats:
		kill_list.append(map_performance_stats[mapName]["kills"])
		death_list.append(map_performance_stats[mapName]["deaths"])
		assist_list.append(map_performance_stats[mapName]["assists"])

	br1 = np.arange(len(kill_list))
	br2 = [x + barWidth for x in br1]
	br3 = [x + barWidth for x in br2]
	plt.bar(br1, kill_list, color="g", width=barWidth, label="Kills")
	plt.bar(br2, death_list, color="r",width=barWidth, label="Deaths")
	plt.bar(br3, assist_list, color="y", width=barWidth, label="Assists")
	plt.xlabel('Map', fontweight ='bold', fontsize = 15)
	plt.ylabel('Num Kills/Deaths/Assists', fontweight ='bold', fontsize = 15)
	plt.xticks([r + barWidth for r in range(len(kill_list))],
        map_performance_stats.keys())
	plt.legend()
	# plt.bar()
	plt.show()

####################################################################
#  Plots average map KDA values as a bar graph                     #
#   															   #
####################################################################
def plot_map_average_kda_stats(map_average_performance_stats):
	barWidth = 0.25
	fig = plt.subplots(figsize =(12, 8))
	kill_list, death_list, assist_list = [], [], []
	for mapName in map_average_performance_stats:
		kill_list.append(map_average_performance_stats[mapName]["average_kills"])
		death_list.append(map_average_performance_stats[mapName]["average_deaths"])
		assist_list.append(map_average_performance_stats[mapName]["average_assists"])

	br1 = np.arange(len(kill_list))
	br2 = [x + barWidth for x in br1]
	br3 = [x + barWidth for x in br2]
	plt.bar(br1, kill_list, color="g", width=barWidth, label="Kills")
	plt.bar(br2, death_list, color="r",width=barWidth, label="Deaths")
	plt.bar(br3, assist_list, color="y", width=barWidth, label="Assists")
	plt.xlabel('Map', fontweight ='bold', fontsize = 15)
	plt.ylabel('Num Kills/Deaths/Assists', fontweight ='bold', fontsize = 15)
	plt.xticks([r + barWidth for r in range(len(kill_list))],
        map_average_performance_stats.keys())
	plt.legend()
	# plt.bar()
	plt.show()

####################################################################
#  Plots other relevant values as a bar graph                      #
#   															   #
####################################################################
def plot_map_other_stats(map_other_stats):
	barWidth = 0.25
	fig = plt.subplots(figsize =(12, 8))
	kpr_list, dpr_list, hsp_list = [], [], []
	for mapName in map_other_stats:
		kpr_list.append(map_other_stats[mapName]["kpr"])
		dpr_list.append(map_other_stats[mapName]["dpr"])
		hsp_list.append(map_other_stats[mapName]["hsp"])

	br1 = np.arange(len(kpr_list))
	br2 = [x + barWidth for x in br1]
	br3 = [x + barWidth for x in br2]
	plt.bar(br1, kpr_list, color="g", width=barWidth, label="Kills per Round")
	plt.bar(br2, dpr_list, color="r",width=barWidth, label="Deaths per Round")
	plt.bar(br3, hsp_list, color="y", width=barWidth, label="HSP")
	plt.xlabel('Map', fontweight ='bold', fontsize = 15)
	plt.ylabel('', fontweight ='bold', fontsize = 15)
	plt.xticks([r + barWidth for r in range(len(kpr_list))],
        map_other_stats.keys())
	plt.legend()
	# plt.bar()
	plt.show()


if __name__=="__main__":
	filename = sys.argv[1] + ".html"
	analyzedPlayer = Player(sys.argv[1])
	with open(filename, 'rb') as html:
		comp_soup = BeautifulSoup(html, "lxml")


	unfiltered_table_rows = comp_soup.find("table", {"class": "generic_kv_table csgo_scoreboard_root"}).find('tbody').find_all('tr', recursive=False)

	#First table row in the table is a header row, contains no data
	del unfiltered_table_rows[0]


	for row in unfiltered_table_rows:
		#Table with class csgo_scoreboard_iner_left contains the map, match time, wait time, match duration, and viewers
		match_overview = row.find("table", {"class": ["csgo_scoreboard_inner_left"]}).find('tbody').find_all('tr')

		# The last row will be Download GOTV Demo. If Demo is no longer available, then the last row will be Viewers. If no viewers, then neither row will exist
		# The row structure will always be
		# Map
		# Time
		# Ranked: Yes/No
		# Wait Time
		# Duration
		# Viewer (May not exist)
		# Download Demo (May not exist)
		if(len(match_overview) == 5 or not match_overview[5].text.strip().startswith("Viewers: ")):
			map_name = match_overview[0].text.strip()
			time = match_overview[1].text.strip()
			# skip index 2 as that's "Is Ranked: Yes" and thus an useless field
			wait_time = match_overview[3].text.strip()
			duration = match_overview[4].text.strip()
			viewer_count = 'Viewers: 0'
		else:
			map_name = match_overview[0].text.strip()
			time = match_overview[1].text.strip()
			wait_time = match_overview[3].text.strip()
			duration = match_overview[4].text.strip()
			viewer_count = match_overview[5].text.strip()

		#Table with class csgo_scoreboard_inner_right contains the actual stats of every person
		scoreboard = row.find("table", {"class": ['csgo_scoreboard_inner_right']}).find('tbody').find_all('tr')
		#As before, first row is a header and contains no useful data
		del scoreboard[0]

		#The element at scoreboard index 5 contains the match score
		round_score_html = scoreboard.pop(5)
		round_score = round_score_html.find('td').text.split(":")

		count = 0
		for player in scoreboard:
			if(player.find("a", {"class": ['linkTitle']}).text != sys.argv[1]):
				count = count + 1
			else:
				stats = player.find_all('td')
				del stats[0]
				ping = stats[0].text.strip()
				kills = stats[1].text.strip()
				assists = stats[2].text.strip()
				deaths = stats[3].text.strip()
				mvps = stats[4].text.strip()
				hsp = stats[5].text.strip()
				score = stats[6].text.strip()
				break
			

		if(count < 5):
			rounds_for = round_score[0].strip()
			rounds_against = round_score[1].strip()
		else:
			rounds_for = round_score[1].strip()
			rounds_against = round_score[0].strip()

		test_match = Match(map_name, time, wait_time, duration, viewer_count, ping, kills, assists, deaths, mvps, hsp, score, rounds_for, rounds_against)
		analyzedPlayer.add_match(test_match)
		match_list.append(test_match)
		

	#Eliminates duplicate maps that occur when the automated javascript scrolling isn't stopped immediately
	for match in match_list:
		if match.map == '':
			pass
		elif match not in updated_match_list:
			updated_match_list.append(match)
		else:
			pass

	# print(len(match_list))
	# print(len(updated_match_list))
	# print(len(unfiltered_table_rows))

	# print(num_wins())
	# print(num_losses())
	# print(num_ties())

	df = pd.DataFrame(m.__dict__ for m in analyzedPlayer.matches)

	# Calculate Winrates of each individual map
	map_stats = {}
	for mapName in analyzedPlayer.get_all_maps():
		mapWins = len(df.loc[(df.map == mapName) & (df.rounds_for > df.rounds_against)])
		mapLosses = len(df.loc[(df.map == mapName) & (df.rounds_for < df.rounds_against)])
		mapTies = len(df.loc[(df.map == mapName) & (df.rounds_for == df.rounds_against)])
		mapSpecificDf = df.loc[(df.map == mapName)]
		map_stats[mapName] = {
			"wins": mapWins,
			"losses": mapLosses,
			"ties": mapTies,
			"total": mapWins+mapLosses+mapTies
		}
	print(map_stats)
	plot_map_win_pct(map_stats)

	# Calculate total + average KDA on each individual map
	kda_stats = {}
	average_kda_per_map_stats = {}
	for mapName in analyzedPlayer.get_all_maps():
		mapDf = df.loc[(df.map == mapName)]
		mapKills = mapDf["kills"].sum()
		mapDeaths = mapDf["deaths"].sum()
		mapAssists = mapDf["assists"].sum()
		kda_stats[mapName] = {
			"kills": mapKills,
			"deaths": mapDeaths,
			"assists": mapAssists
		}
		average_kda_per_map_stats[mapName] = {
			"average_kills": mapKills/len(mapDf),
			"average_deaths": mapDeaths/len(mapDf),
			"average_assists": mapAssists/len(mapDf)
		}
	
	print(kda_stats)
	plot_map_kda_stats(kda_stats)
	print(average_kda_per_map_stats)
	plot_map_average_kda_stats(average_kda_per_map_stats)

	# Calculate other stats - KPR/DPR/HSP
	other_stats_map = {}
	for mapName in analyzedPlayer.get_all_maps():
		mapDf = df.loc[(df.map == mapName)]
		mapKills = mapDf["kills"].sum()
		mapDeaths = mapDf["deaths"].sum()
		mapHeadshotKills = mapDf["headshot_kills"].sum()
		mapRounds = mapDf["rounds_for"].sum() + mapDf["rounds_against"].sum()
		other_stats_map[mapName] = {
			"kpr": mapKills/mapRounds,
			"dpr": mapDeaths/mapRounds,
			"hsp": mapHeadshotKills/mapKills
		}

	plot_map_other_stats(other_stats_map)

	# Calculate line graph over time of KDA and HSP


	'''with open('matches.csv', 'w', newline = '') as csv_file:
		writer = csv.writer(csv_file)
		for match in updated_match_list:
			if(match.rounds_for == match.rounds_against):
				writer.writerow([match.map, match.time, match.wait_time, match.duration, match.viewer_count, match.ping, 
								match.kills, match.assists, match.deaths, match.hsp, match.score, match.rounds_for, match.rounds_against])'''