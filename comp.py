from bs4 import BeautifulSoup
import lxml
import matplotlib
import time
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import csv
import sys
import datetime
import time
from datetime import timedelta

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
		self.kills = kills
		self.assists = assists 
		self.deaths = deaths
		self.mvp_count = mvp_count
		self.hsp = hsp
		self.score = score
		self.rounds_for = rounds_for
		self.rounds_against = rounds_against

	def __eq__(self, other):
		return self.__dict__ == other.__dict__


start = time.time()
with open("ZerO_Comp_Data.html", 'rb') as html:
	comp_soup = BeautifulSoup(html, "lxml")
print(time.time() - start)

unfiltered_table_rows = comp_soup.find("table", {"class": "generic_kv_table csgo_scoreboard_root"}).find('tbody').find_all('tr', recursive=False)
del unfiltered_table_rows[0]

for row in unfiltered_table_rows:
	match_overview = row.find("table", {"class": ["csgo_scoreboard_inner_left"]}).find('tbody').find_all('tr')

	if(len(match_overview) == 4):
		map_name = match_overview[0].text.strip()
		time = match_overview[1].text.strip()
		wait_time = match_overview[2].text.strip()
		duration = match_overview[3].text.strip()
		viewer_count = '0'
	else:
		map_name = match_overview[0].text.strip()
		time = match_overview[1].text.strip()
		wait_time = match_overview[2].text.strip()
		duration = match_overview[3].text.strip()
		viewer_count = match_overview[4].text.strip()

	scoreboard = row.find("table", {"class": ['csgo_scoreboard_inner_right']}).find('tbody').find_all('tr')
	del scoreboard[0]

	round_score_html = scoreboard.pop(5)
	round_score = round_score_html.find('td').text.split(":")
	count = 0
	for player in scoreboard:
		if(player.find("a", {"class": ['linkTitle']}).text != "ZerO_0 hellcase.com"):
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
	match_list.append(test_match)
	print(map_name, time, wait_time, duration, viewer_count, ping, kills, assists, deaths, mvps, hsp, score, rounds_for, rounds_against)

for match in match_list:
	if match.map == '':
		pass
	elif match not in updated_match_list:
		updated_match_list.append(match)
	else:
		pass

print(len(match_list))
print(len(updated_match_list))
print(len(unfiltered_table_rows))
