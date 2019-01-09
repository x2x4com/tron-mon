#!/usr/bin/env python
# encoding: utf-8
# ===============================================================================
#
#         FILE:
#
#        USAGE:
#
#  DESCRIPTION:
#
#      OPTIONS:  ---
# REQUIREMENTS:  ---
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  YOUR NAME (),
#      COMPANY:
#      VERSION:  1.0
#      CREATED:
#     REVISION:  ---
# ===============================================================================
# 找信息文件
# 匹配进程
# 检查进程是否正常 - 进程是否在， 端口是否在, 块是不是在增长
import psutil
import subprocess
import os
import sys
import json
import multiprocessing as mp
import socket
import requests
import re
from cfg import node, log_file, thread_timeout, kill_try, kill_wait
from time import time, sleep
import log


stats_structs = {
    "pid": -1,
    "block": {
        "last": 0,
        "count": 0
    }
}


def check_cfg():
    log.debug("Check cfg")
    for n in node:
        must_existed(node[n]["runtime_dir"], True)
        must_existed(node[n]["config"])
        must_existed(node[n]["jar"])
        must_existed(node[n]["data"], True)


def is_existed(t: str):
    return os.path.exists(t)


def must_existed(t: str, w: bool=False):
    if not is_existed(t):
        raise ValueError("%s not existed" % t)
    if w:
        if not os.access(t, os.W_OK):
            raise ValueError("%s can not write" % t)


def save_stats(f: str, d: dict):
    with open(f, 'rw') as fd:
        json.dump(fd, d)


def load_stats(f: str):
    if is_existed(f):
        with open(f, 'r') as fd:
            return json.load(fd)
    return stats_structs


def run_node(java_opts: str, jar: str, config: str, data: str, runtime_dir: str="/tmp"):
    cmd = "exec java {java_opts} -jar {jar} -c {config} --witness -d {data}".format(
        java_opts=java_opts,
        config=config,
        jar=jar,
        data=data
    )
    return subprocess.Popen(cmd, cwd=runtime_dir, shell=True, stdout=subprocess.PIPE)


def run():
    log.debug("Start running...")
    start = time()
    worker_list = []
    for n in node:
        log.debug("Check %s" % n)
        process = mp.Process(target=check_node, args=(n,))
        process.start()
        worker_list.append(process)
    while time() - start <= thread_timeout:
        if any(p.is_alive() for p in worker_list):
            sleep(.1)
        else:
            break
    else:
        log.error("timed out, killing all processes")
        for p in worker_list:
            p.terminate()
            p.join()


def check_node(n):
    start_node = False
    has_port_http = False
    # has_port_rpc = False
    has_pid = False
    node_info = node[n]
    stats = load_stats(node_info['stats'])
    if check_port(node_info['http']):
        has_port_http = True
    # if check_port(node_info['rpc']):
    #     has_port_rpc = True
    if check_pid(stats['pid']):
        # 进程存在，检查一下端口是否在
        has_pid = True
    last_block = get_last_block('http://127.0.0.1:%s%s' % (node_info['http'], node_info['api_get_now_block']))
    if last_block > 0:
        d = stats_structs.copy()
        log.info("[%s] save block %d", (n, last_block))
        d['block']['last'] = last_block
        # todo 多少块不同步，强制重启
        # if stats['block']['count'] > 100:
        #     kill_by_pid(stats['pid'], node_info['stop_signal'])
        #     if any([check_port(node_info['http']), check_port(node_info['rpc'])]):
        #         log.error("%s port in use" % n)
        #         raise SystemExit("%s port in use" % n)
        #     start_node = True
        if last_block == stats['block']['last']:
            d['block']['count'] += stats['block']['count']
        if has_pid:
            d['pid'] = stats['pid']
        else:
            d['pid'] = find_pid_by_port(node_info['http'])
        save_stats(node_info['stats'], d)
    else:
        log.warning('[%s] can not get last block' % n)
        pid = -1
        # need to restart
        if has_pid:
            pid = stats['pid']
        else:
            if has_port_http:
                pid = find_pid_by_port(node_info['http'])
        if pid > 0:
            kill_by_pid(pid, node_info['stop_signal'])
        # start new
        # confirm
        if any([check_port(node_info['http']), check_port(node_info['rpc'])]):
            log.error("%s port in use" % n)
            raise SystemExit("%s port in use" % n)
        start_node = True
    if start_node:
        _process = run_node(
            jar=node_info['jar'],
            java_opts=node_info['java_opts'],
            config=node_info['config'],
            data=node_info['data'],
            runtime_dir=node_info['runtime_dir']
        )
        d = stats_structs.copy()
        d['pid'] = _process.pid
        save_stats(node_info['stats'], d)
        log.info('[%s] started pid=%d' % (n, d['pid']))


def kill_by_pid(pid, sig):
    _kill = 0
    while _kill < kill_try:
        if check_pid(pid):
            os.kill(pid, sig)
        else:
            break
        _kill += 1
        sleep(kill_wait)
    else:
        # force kill
        os.kill(pid, 9)
        sleep(10)


def find_pid_by_port(port: int):
    cmd = "netstat -lntp | grep ':%d'" % port
    # port_regex = re.compile('^tcp6\s+0\s+0\s+:::%d\s+:::\*\s+LISTEN\s+(\d+)/java' % port)
    port_regex = re.compile('.*\s+LISTEN\s+(\d+)/\w+')
    _process = subprocess.Popen(cmd, bufsize=4096, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    _process.wait()
    rt = _process.stdout.read().decode()
    find_all = port_regex.findall(rt)
    if len(find_all) > 0:
        return find_all[0]
    return -1


def get_last_block(url: str):
    block_now = 0
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        block_now = data['block_header']['raw_data']['number']
    except ConnectionError:
        log.error("%s ConnectionError" % url)
    except requests.ReadTimeout:
        log.error("%s ReadTimeout" % url)
    except json.JSONDecodeError:
        log.error("%s JSONDecodeError" % url)
    except KeyError:
        log.error("%s KeyError" % url)
    return block_now


def check_port(port: int):
    log.debug("Check port %d" % port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    if result == 0:
        return True
    return False


def check_pid(pid: int):
    log.debug("Check pid %d" % pid)
    return psutil.pid_exists(pid)


def main():
    log_level = 'INFO'
    if len(sys.argv) > 1:
        if sys.argv[1] in ['d', 'debug', 'DEBUG']:
            log_level = 'DEBUG'
    else:
        log_level = os.environ.get("TRON-MON-LOG", "INFO")
    log.set_logger(filename=log_file, level=log_level, console=True)
    check_cfg()
    run()


if __name__ == '__main__':
    main()