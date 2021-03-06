cryptocurrency-tools
====================

`btce_monitor.py`
-----------------
A Python script to track fluctuations in [btc-e.com](https://btc-e.com) exchange rates using their API. Monitor any BTCe currency pair with visual and audible alerts at customisable thresholds.

<img src="https://raw.github.com/bede/cryptocurrency-tools/master/screenshot.png" style="width:459px;height:235px;">

**Installation**  
This script uses the Python requests module. To install this, you need PIP, the Python package manager.  
– on OS X: `sudo easy_install pip`  
– on Debian/Ubuntu: `sudo apt-get install python-pip`  

Next install the requests module:  
`sudo pip install requests`  

That should be it. Run `python btce_monitor.py` or `python btce_monitor.py --help` to get started

**Updates**  
2013-12-29: Rewrote as OOP, as an exercise
