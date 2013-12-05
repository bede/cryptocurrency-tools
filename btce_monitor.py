#!/usr/bin/python

import sys
import time
import requests
import argparse

parser = argparse.ArgumentParser(description="Monitor the exchange rate of a BTCe currency pair with visual and audible alerts at customisable thresholds")
parser.add_argument('-c', '--currency_pair', default='ltc/btc', help='Any BTCe traded currency pair, defaults to \'btc/ltc\'')
parser.add_argument('-n', '--notify_threshold', type=float, default='0.1', help='Percentage change that triggers a console notification')
parser.add_argument('-a', '--alert_threshold', type=float, default='2', help='Percentage change that also triggers an audible notification')
arguments = parser.parse_args()

polling_interval = 10 # Too low and your IP will be banned
currency_pair_name = arguments.currency_pair.upper()
currency_pair_url = 'https://btc-e.com/api/2/' + arguments.currency_pair.replace('/', '_') + '/ticker'
notify_threshold = arguments.notify_threshold
alert_threshold = arguments.alert_threshold

def get_percent_change(initial_price, current_price):
	percent_change = round(((current_price-initial_price)/initial_price)*100, 2)
	if percent_change > 0:
		percent_change = '+' + str(percent_change) + '%'
	elif percent_change < 0:
		percent_change =  str(percent_change) + '%'
	else:
		percent_change = ''
	return percent_change

def alert(direction): # Like notify(), but also plays a sound (tested on OS X)
	if direction is 'up':
		arrow_char = u'\u2b06'
	elif direction is 'down':
		arrow_char = u'\u2b07'
	print (arrow_char + ' ' + str(current_price) + ' ' + currency_pair_name + ' '
		+ get_percent_change(initial_price, current_price) + ' *alert triggered*') 
	for i in range(0,5):
		sys.stdout.write('\a')
		sys.stdout.flush()
		time.sleep(0.2)

def notify(direction):
	if direction is 'up':
		arrow_char = u'\u2b06'
	elif direction is 'down':
		arrow_char = u'\u2b07'
	print (arrow_char + ' ' + str(current_price) + ' ' + currency_pair_name + ' '
		+ get_percent_change(initial_price, current_price))

def initialise():
	global initial_price
	global last_price
	r = requests.get(currency_pair_url)
	initial_price = float(r.json()['ticker']['last'])
	last_price = initial_price
	if len(sys.argv) is 1:
		print 'No arguments were supplied. Try running \'btce_monitor.py --help\''
	print 'Notification threshold: ' + str(notify_threshold) + '%'
	print 'Audible alert threshold: ' + str(alert_threshold) + '%'
	print 'Reference price: ' + str(initial_price) + ' ' + currency_pair_name

def check_rate():
	global current_price
	global last_price	
	r = requests.get(currency_pair_url)
	current_price = float(r.json()['ticker']['last'])
	if current_price >= initial_price*(1+(alert_threshold/100)):
		alert('up')
		last_price = current_price
	elif current_price <= initial_price*(1-(alert_threshold/100)):
		alert('down')
		last_price = current_price
	elif current_price >= last_price*(1+(notify_threshold/100)):
		notify('up')
		last_price = current_price
	elif current_price <= last_price*(1-(notify_threshold/100)):
		notify('down')
		last_price = current_price

initialise()
time.sleep(polling_interval)
while True:
	check_rate()
	time.sleep(polling_interval)