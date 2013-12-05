cryptocurrency-tools
====================

`btce_monitor.py`
-----------------
A crude script to provide alerts of exchange rate flutuations. Monitor any BTCe currency pair with visual and audible alerts at chosen thresholds. Sample output:
```
bede-rmbp:cryptocurrency-tools bede$ ./btce_monitor.py 0.1 1
Notification threshold: 0.1%
Audible alert threshold: 1.0%
Starting at 0.0378 LTC/BTC
⬇ 0.03757 LTC/BTC -0.61%
⬆ 0.03797 LTC/BTC +0.45%
⬇ 0.03756 LTC/BTC -0.63%
⬆ 0.03795 LTC/BTC +0.4%
⬇ 0.03754 LTC/BTC -0.69%
⬆ 0.03791 LTC/BTC +0.29%
⬇ 0.03782 LTC/BTC +0.05%
```
