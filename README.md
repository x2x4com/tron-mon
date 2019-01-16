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

   This script will monitor the [java-tron release page](https://github.com/tronprotocol/java-tron/releases) and automatically download the latest release and make a soft link.

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

5. Test
   ```bash
   $ python3 tron_check_update.py
   Name: Odyssey-v3.2.4
   Create dir: /data/tron/update/3.2.4
   List download:
   [0] download FullNode.jar to /data/tron/update/3.2.4/FullNode.jar
   [################################] 57748/57748 - 00:00:08
   [1] download md5sum.txt to /data/tron/update/3.2.4/md5sum.txt
   [################################] 1/1 - 00:00:00
   [2] download SolidityNode.jar to /data/tron/update/3.2.4/SolidityNode.jar
   [################################] 57748/57748 - 00:00:05
   md5 check
   check FullNode.jar
   check SolidityNode.jar
   latest ver dir is 3.2.4
   remove link /data/tron/tron_nodes/fullnode/full.jar
   /data/tron/update/3.2.4/FullNode.jar => /data/tron/tron_nodes/fullnode/full.jar
   remove link /data/tron/tron_nodes/soliditynode/solidity.jar
   /data/tron/update/3.2.4/SolidityNode.jar => /data/tron/tron_nodes/soliditynode/solidity.jar
   ```
   ```bash
   python3 tron_mon.py d
   ```
   
   Nothing return is normal, you need check logfile
   ```bash
   2019-01-16 06:25:41,376 [DEBUG] tron_mon.py[line:49] Check cfg
   2019-01-16 06:25:41,376 [DEBUG] tron_mon.py[line:96] Start running...
   2019-01-16 06:25:41,376 [DEBUG] tron_mon.py[line:100] Check full
   2019-01-16 06:25:41,381 [DEBUG] tron_mon.py[line:100] Check solidity
   2019-01-16 06:25:41,382 [DEBUG] tron_mon.py[line:123] load stats file
   2019-01-16 06:25:41,382 [DEBUG] tron_mon.py[line:125] stats {'pid': 2611, 'block': {'last': 5796894, 'count': 0, 'tron_api_last': 0}}
   2019-01-16 06:25:41,383 [DEBUG] tron_mon.py[line:126] check port 8500
   2019-01-16 06:25:41,383 [DEBUG] tron_mon.py[line:243] Check port 8500
   2019-01-16 06:25:41,383 [DEBUG] tron_mon.py[line:131] check pid 2611
   2019-01-16 06:25:41,383 [DEBUG] tron_mon.py[line:252] Check pid 2611
   2019-01-16 06:25:41,384 [DEBUG] tron_mon.py[line:135] get last block
   2019-01-16 06:25:41,384 [DEBUG] tron_mon.py[line:123] load stats file
   2019-01-16 06:25:41,385 [DEBUG] tron_mon.py[line:125] stats {'pid': 2612, 'block': {'last': 5792843, 'count': 0, 'tron_api_last': 0}}
   2019-01-16 06:25:41,385 [DEBUG] tron_mon.py[line:126] check port 8600
   2019-01-16 06:25:41,385 [DEBUG] tron_mon.py[line:243] Check port 8600
   2019-01-16 06:25:41,386 [DEBUG] tron_mon.py[line:131] check pid 2612
   2019-01-16 06:25:41,386 [DEBUG] tron_mon.py[line:252] Check pid 2612
   2019-01-16 06:25:41,386 [DEBUG] tron_mon.py[line:135] get last block2019-01-16 06:25:41,392 [DEBUG] connectionpool.py[line:205] Starting new HTTP connection (1): 127.0.0.1:8600
   2019-01-16 06:25:41,389 [DEBUG] connectionpool.py[line:205] Starting new HTTP connection (1): 127.0.0.1:8500
   2019-01-16 06:25:41,412 [DEBUG] connectionpool.py[line:393] http://127.0.0.1:8600 "GET /walletsolidity/getnowblock HTTP/1.1" 200 None
   2019-01-16 06:25:41,415 [DEBUG] tron_mon.py[line:138] last block 5792843
   2019-01-16 06:25:41,415 [INFO] tron_mon.py[line:141] [solidity] save block 5792843
   2019-01-16 06:25:41,415 [DEBUG] tron_mon.py[line:151] block same
   2019-01-16 06:25:41,415 [DEBUG] tron_mon.py[line:157] save {'pid': 2612, 'block': {'last': 5792843, 'count': 0, 'tron_api_last': 0}}
   2019-01-16 06:25:41,413 [DEBUG] connectionpool.py[line:393] http://127.0.0.1:8500 "GET /wallet/getnowblock HTTP/1.1" 200 None
   2019-01-16 06:25:41,416 [DEBUG] tron_mon.py[line:138] last block 5796894
   2019-01-16 06:25:41,416 [INFO] tron_mon.py[line:141] [full] save block 5796894
   2019-01-16 06:25:41,416 [DEBUG] tron_mon.py[line:151] block same
   2019-01-16 06:25:41,417 [DEBUG] tron_mon.py[line:157] save {'pid': 2611, 'block': {'last': 5796894, 'count': 0, 'tron_api_last': 0}}

   ``` 
   
   looks good.

6. Config crontab

   Here is example for user's crontab
   
   ```
   */5 * * * * $HOME/tron-mon/bin/python3 $HOME/tron-mon/src/tron_mon.py
   0 1 * * * $HOME/tron-mon/bin/python3 $HOME/tron-mon/src/tron_check_update.py 2>&1 >>/dev/null
   ```

7. Check log file
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
