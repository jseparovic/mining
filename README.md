# mining related scripts


### t-rex-rate.py

calculates average hash rate per GPU per coin from hiveos t-rex log file. Useful for checking hashrate for dual LHR mode

Example:
```
# for i in 3 4 5 6; do ssh user@rig-2-1-$i rate.py; done
{'rig-2-1-3': [{'ERG': 157.68}, {'ETH': 26.93}]}
{'rig-2-1-4': [{'ERG': 155.59}, {'ETH': 27.56}]}
{'rig-2-1-5': [{'ERG': 154.37}, {'ETH': 28.22}]}
{'rig-2-1-6': [{'ERG': 157.58}, {'ETH': 26.99}]}
```
