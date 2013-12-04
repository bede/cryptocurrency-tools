#!/usr/bin/python

import sys
import time
import requests

alert_threshold = float(sys.argv[1])
notify_threshold = float(sys.argv[2])
currency_pair_name = ' ' + 'LTC/BTC'
currency_pair_url = 'https://btc-e.com/api/2/ltc_btc/ticker'
polling_interval = 5
initial_price = None
current_price = None
last_price = None

def alert(direction=None):
	global last_price
	if direction is 'up':
		print u'\u2b06 ' + str(current_price) + currency_pair_name +  ' - alert'
	elif direction is 'down':
		print u'\u2b07 ' + str(current_price) + currency_pair_name + ' - alert'
	for i in range(0,5):
		sys.stdout.write('\a')
		sys.stdout.flush()
	last_price = current_price

def notify(direction):
	global last_price
	if direction is 'up':
		print u'\u2b06 ' + str(current_price) + currency_pair_name
	elif direction is 'down':
		print u'\u2b07 ' + str(current_price) + currency_pair_name
	elif direction is 'none':
		print str(initial_price) + currency_pair_name
	last_price = current_price

def fetch_initial_price():
	global initial_price
	global last_price
	r = requests.get(currency_pair_url)
	initial_price = float(r.json()['ticker']['last'])
	last_price = initial_price
	notify('none')
	time.sleep(polling_interval)

def check_current_price():
	global current_price
	global last_price	
	r = requests.get(currency_pair_url)
	current_price = float(r.json()['ticker']['last'])
	if current_price > initial_price*(1+alert_threshold):
		alert('up')
	elif current_price < initial_price*(1-alert_threshold):
		alert('down')
	elif current_price > last_price*(1+notify_threshold):
		notify('up')
	elif current_price < last_price*(1-notify_threshold):
		notify('down')
		
fetch_initial_price()
while True:
	check_current_price()
	time.sleep(polling_interval)