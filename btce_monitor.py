#!/usr/bin/env python

import sys
import time
import requests
import argparse
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
log = logging.getLogger("BTCEMonitor")


class ExchangeRate(object):
    currency_pair_url = 'https://btc-e.com/api/2/%s/ticker'
        
    def __init__(self, currency_pair_name):
        self.currency_pair_name = currency_pair_name.replace('/', '_')   

        
    def getCurrentPrice(self):        
        r = requests.get(self.currency_pair_url % self.currency_pair_name)
        return float(r.json()['ticker']['last'])



class BTCEMonitor(object):    
    polling_interval = 30 # Too low and your IP will be banned
    initial_price = None

    def __init__(self, currency_pair_name, notify_threshold, alert_threshold):        
        self.currency_pair_name = currency_pair_name
        self.notify_threshold = notify_threshold
        self.alert_threshold = alert_threshold
        
    
    def run(self):
        while True:
            self.check_rate()
            time.sleep(self.polling_interval)
            
    
    def check_rate(self):
        exchRate = ExchangeRate(self.currency_pair_name)
        self.current_price = exchRate.getCurrentPrice()
        
        if (self.initial_price is None):
            self.initial_price = self.current_price
            self.last_price = self.current_price
            
        log.debug('Current price: %f' % self.current_price)            
            
        if self.current_price >= self.initial_price*(1+(self.alert_threshold/100)):            
            self.alert('up')
            self.last_price = self.current_price
        elif self.current_price <= self.initial_price*(1-(self.alert_threshold/100)):
            self.alert('down')
            self.last_price = self.current_price
        elif self.current_price >= self.last_price*(1+(self.notify_threshold/100)):
            self.notify('up')
            self.last_price = self.current_price
        elif self.current_price <= self.last_price*(1-(self.notify_threshold/100)):
            self.notify('down')
            self.last_price = self.current_price
            
            
    def get_percent_change(self):
        percent_change = round(((self.current_price-self.initial_price)/self.initial_price)*100, 2)
        if percent_change > 0:
            percent_change = '+' + str(percent_change) + '%'
        elif percent_change < 0:
            percent_change =  str(percent_change) + '%'
        else:
            percent_change = ''
        return percent_change            
            
            
    def alert(self, direction): # Like notify(), but also plays a sound (tested on OS X)
        if direction is 'up':
            arrow_char = u'\u2b06'
        elif direction is 'down':
            arrow_char = u'\u2b07'
        print (arrow_char + ' ' + str(self.current_price) + ' ' + self.currency_pair_name.upper() + ' '
            + self.get_percent_change() + ' *alert triggered*') 
        for i in range(0,5):
            sys.stdout.write('\a')
            sys.stdout.flush()
            time.sleep(0.2)
            
    
    def notify(self, direction):
        if direction is 'up':
            arrow_char = u'\u2b06'
        elif direction is 'down':
            arrow_char = u'\u2b07'
        print (arrow_char + ' ' + str(self.current_price) + ' ' + self.currency_pair_name + ' '
            + self.get_percent_change(self.initial_price, self.current_price))


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description="Monitor the exchange rate of a BTCe currency pair with visual and audible alerts at customisable thresholds")
    parser.add_argument('-c', '--currency_pair', default='ltc/btc', help='Any BTCe traded currency pair, defaults to \'btc/ltc\'')
    parser.add_argument('-n', '--notify_threshold', type=float, default='0.1', help='Percentage change that triggers a console notification')
    parser.add_argument('-a', '--alert_threshold', type=float, default='2', help='Percentage change that also triggers an audible notification')
    arguments = parser.parse_args()
    
    monitor = BTCEMonitor(arguments.currency_pair, arguments.notify_threshold, arguments.alert_threshold)
    monitor.run()
    
    
