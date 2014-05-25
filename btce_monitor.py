#!/usr/bin/env python

import sys
import time
import argparse
import requests


class ExchangeRateAPI(object):
    currency_pair_url = 'https://btc-e.com/api/2/%s/ticker'
    
    def __init__(self, currency_pair_name):
        self.currency_pair_name = currency_pair_name.replace('/', '_')
    
    def current_rate(self):        
        r = requests.get(self.currency_pair_url % self.currency_pair_name)
        return float(r.json()['ticker']['last'])


class ExchangeRateMonitor(object):    
    polling_interval = 10
    initial_rate = None

    def __init__(self, currency_pair_name, notify_threshold, alert_threshold):        
        self.currency_pair_name = currency_pair_name
        self.notify_threshold = notify_threshold
        self.alert_threshold = alert_threshold

        print 'Notification threshold: ' + str(self.notify_threshold) + '%'
        print 'Audible alert threshold: ' + str(self.alert_threshold) + '%'

    def loop(self):
        while True:
            self.check_rate()
            time.sleep(self.polling_interval)

    def check_rate(self):
        btce_api = ExchangeRateAPI(self.currency_pair_name)
        self.current_rate = btce_api.current_rate()
        
        if (self.initial_rate is None):
            self.initial_rate = self.current_rate
            self.last_rate = self.current_rate
            print 'Reference price: ' + str(self.initial_rate) + ' ' + self.currency_pair_name

        if self.current_rate >= self.initial_rate*(1+(self.alert_threshold/100)):            
            self.notify('up', True)
            self.last_rate = self.current_rate
        elif self.current_rate <= self.initial_rate*(1-(self.alert_threshold/100)):
            self.notify('down', True)
            self.last_rate = self.current_rate
        elif self.current_rate >= self.last_rate*(1+(self.notify_threshold/100)):
            self.notify('up')
            self.last_rate = self.current_rate
        elif self.current_rate <= self.last_rate*(1-(self.notify_threshold/100)):
            self.notify('down')
            self.last_rate = self.current_rate
             
    def percent_change(self):
        percent_change = round(((self.current_rate-self.initial_rate)/self.initial_rate)*100, 2)
        if percent_change > 0:
            percent_change = '+' + str(percent_change) + '%'
        elif percent_change < 0:
            percent_change =  str(percent_change) + '%'
        else:
            percent_change = ''
        return percent_change            
    
    def notify(self, direction, audible=False):
        if direction == 'up':
            arrow_char = u'\u2b06'
        elif direction == 'down':
            arrow_char = u'\u2b07'
        print (arrow_char + ' ' + str(self.current_rate) + ' ' + self.currency_pair_name + ' '
            + self.percent_change())
        if audible:
            for i in range(0,5):
                sys.stdout.write('\a')
                sys.stdout.flush()
                time.sleep(0.2)


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description="Monitor the exchange rate of a BTCe currency pair with visual and audible alerts at chosen thresholds")
    parser.add_argument('-c', '--currency_pair', default='ltc/btc', help='Any BTCe traded currency pair, defaults to \'ltc/btc\'')
    parser.add_argument('-n', '--notify_threshold', type=float, default='0.1', help='Percentage change that triggers a console notification')
    parser.add_argument('-a', '--alert_threshold', type=float, default='2', help='Percentage change that also triggers an audible notification')
    arguments = parser.parse_args()
    
    if len(sys.argv) == 1:
        print 'No arguments were supplied. Try running \'btce_monitor.py --help\''

    btce_monitor = ExchangeRateMonitor(arguments.currency_pair, arguments.notify_threshold, arguments.alert_threshold)
    btce_monitor.loop()
    
