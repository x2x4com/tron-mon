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
        'stats': '/data/tron/mon/full-runtime.info',
        'release_name': 'FullNode.jar'
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
        'stats': '/data/tron/mon/solidity-runtime.info',
        'release_name': 'SolidityNode.jar'
    },
}

tron_api = "https://api.trongrid.io"
log_file = '/data/tron/mon/runtime.log'
thread_timeout = 180
kill_try = 10
kill_wait = 6
console_log = False
java_tron_release = "https://api.github.com/repos/tronprotocol/java-tron/releases"
bin_location = "/data/tron/update"
