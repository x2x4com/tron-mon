# tron-mon

These scripts are designed to address tron node monitoring and update issues

The directory structure in the configuration file is set according to [tron-cli](https://github.com/tronprotocol/tron-cli)

## Depend

- [tron-cli](https://github.com/tronprotocol/tron-cli) directory structure 
- Python3.5+

## Introduction
1. tron_mon.py
   
   This script is used to monitor whether the tron's java process is lost, and the block height is growing normally.

2. tron_check_update.py

   This script will monitor the java-tron release page and automatically download the latest release and make a soft link.

## How to use
1. Create a python virtual environment
```bash
cd $HOME
python3 -m venv tron-mon
```

2. Clone the code
```bash
cd $HOME/tron-mon
git clone https://github.com/x2x4com/tron-mon.git src
```

3. Install depends
```bash
. bin/activate
cd src && pip install -r requirements.txt
```

4. Config scripts
Modify the parameters in cfg.py


5. Config crontab
Here is example for user's crontab
```
*/5 * * * * $HOME/tron-mon/bin/python3 $HOME/tron-mon/src/tron_mon.py
0 1 * * * $HOME/tron-mon/bin/python3 $HOME/tron-mon/src/tron_check_update.py 2>&1 >>/dev/null
```

6. Check log file
Check log file in cfg.py
```bash
$ tail -100 /data/tron/mon/runtime.log
2019-01-15 09:50:03,856 [INFO] tron_mon.py[line:141] [full] save block 5792073
2019-01-15 09:50:03,948 [INFO] tron_mon.py[line:141] [solidity] save block 5792054
2019-01-15 09:55:03,654 [INFO] tron_mon.py[line:141] [full] save block 5792142
2019-01-15 09:55:03,668 [INFO] tron_mon.py[line:141] [solidity] save block 5792121
2019-01-15 10:00:04,389 [INFO] tron_mon.py[line:141] [full] save block 5792210
2019-01-15 10:00:04,394 [INFO] tron_mon.py[line:141] [solidity] save block 5792191
2019-01-15 10:05:03,160 [INFO] tron_mon.py[line:141] [full] save block 5792276
2019-01-15 10:05:03,166 [INFO] tron_mon.py[line:141] [solidity] save block 5792256
2019-01-15 10:10:03,745 [INFO] tron_mon.py[line:141] [full] save block 5792332
2019-01-15 10:10:03,753 [INFO] tron_mon.py[line:141] [solidity] save block 5792313
```
