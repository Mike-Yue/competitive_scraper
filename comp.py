from bs4 import BeautifulSoup
import lxml
import matplotlib.pyplot as plt
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

def plot_map_win_pct():
	mirage_counter = 0
	mirage_win_counter = 0
	inferno_counter = 0
	inferno_win_counter = 0
	dust2_counter = 0
	dust2_win_counter = 0
	cache_counter = 0
	cache_win_counter = 0
	cbble_counter = 0
	cbble_win_counter = 0
	overpass_counter = 0
	overpass_win_counter = 0

	for match in updated_match_list:
		if(match.map == 'Competitive Mirage'):
			mirage_counter = mirage_counter + 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				mirage_win_counter = mirage_win_counter + 1
		if(match.map == 'Competitive Inferno'):
			inferno_counter = inferno_counter + 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				inferno_win_counter = inferno_win_counter + 1
		if(match.map == 'Competitive Dust II'):
			dust2_counter = dust2_counter + 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				dust2_win_counter = dust2_win_counter + 1
		if(match.map == 'Competitive Cache'):
			cache_counter = cache_counter + 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				cache_win_counter = cache_win_counter + 1
		if(match.map == 'Competitive Cobblestone'):
			cbble_counter = cbble_counter + 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				cbble_win_counter = cbble_win_counter + 1
		if(match.map == 'Competitive Overpass'):
			overpass_counter = overpass_counter + 1
			if(int(match.rounds_for) > int(match.rounds_against)):
				overpass_win_counter = overpass_win_counter + 1

	y = [mirage_win_counter/mirage_counter, inferno_win_counter/inferno_counter, dust2_win_counter/dust2_counter, cache_win_counter/cache_counter, cbble_win_counter/cbble_counter, overpass_win_counter/overpass_counter]
	x = ['Mirage', 'Inferno', 'Dust II', 'Cache', 'Cobblestone', 'Overpass']
	print(y)
	plt.bar(x, y)
	plt.show()


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

print(num_wins())
print(num_losses())
print(num_ties())

plot_map_win_pct()


'''with open('matches.csv', 'w', newline = '') as csv_file:
	writer = csv.writer(csv_file)
	for match in updated_match_list:
		if(match.rounds_for == match.rounds_against):
			writer.writerow([match.map, match.time, match.wait_time, match.duration, match.viewer_count, match.ping, 
							match.kills, match.assists, match.deaths, match.hsp, match.score, match.rounds_for, match.rounds_against])'''