#!/usr/bin/env python
# encoding: utf-8

node = {
    "full": {
        "java_opts": "-Xmx6g -XX:+HeapDumpOnOutOfMemoryError",
        "runtime_dir": "/data/tron/tron_nodes/fullnode",
        "config": "/data/tron/tron_nodes/fullnode/full.conf",
        "jar": "/data/tron/tron_nodes/fullnode/full.jar",
        "data": "/data/tron/tron_nodes/fullnode/data",
        "api_get_now_block": "/wallet/getnowblock",
        'stop_signal': 15,
        'http': 8500,
        'rpc': 58500,
        'stats': '/data/tron/mon/full-runtime.info'
    },
    "solidity": {
        "java_opts": "-Xmx6g -XX:+HeapDumpOnOutOfMemoryError",
        "runtime_dir": "/data/tron/tron_nodes/soliditynode",
        "config": "/data/tron/tron_nodes/soliditynode/sol.conf",
        "jar": "/data/tron/tron_nodes/soliditynode/solidity.jar",
        "data": "/data/tron/tron_nodes/soliditynode/data",
        "api_get_now_block": "/walletsolidity/getnowblock",
        'stop_signal': 15,
        'http': 8600,
        'rpc': 58600,
        'stats': '/data/tron/mon/solidity-runtime.info'
    },
}

tron_api = "https://api.trongrid.io"
log_file = '/tmp/mon.log'
thread_timeout = 180
kill_try = 10
kill_wait = 6
