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
import requests
# import json
# import multiprocessing as mp
import re
import os
from hashlib import md5
from clint.textui import progress
from tron_mon import must_existed, is_existed
from cfg import java_tron_release, bin_location, node


def arrange_node():
    o = {}
    for n in node:
        release = node[n]['release_name']
        jar = node[n]['jar']
        o[release] = jar
    return o


def check_update():
    resp = requests.get(java_tron_release)
    data = resp.json()
    return data[0]


def download(url, t):
    r = requests.get(url, stream=True)
    with open(t, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()


def get_version(tag):
    reg_ver = re.compile('^\w+-v(.*)$')
    find_all = reg_ver.findall(tag)
    if len(find_all) > 0:
        return find_all[0]
    return None


def find_last():
    dirs = os.listdir(bin_location)
    m = '0.0.0'
    for d in dirs:
        m = _mp(m, d)
    return m


def _mp(s1, s2):
    s1s = [int(x) for x in s1.split('.')]
    s2s = [int(x) for x in s2.split('.')]
    if s1s[0] == s2s[0]:
        if s1s[1] == s2s[1]:
            if s1s[2] > s2s[2]:
                return s1
            return s2
        if s1s[1] > s2s[1]:
            return s1
        return s2
    if s1s[0] > s2s[0]:
        return s1
    return s2


def remove_link(t):
    if os.path.isfile(t):
        return os.remove(t)
    if os.path.islink(t):
        return os.unlink(t)


def make_link(f, t):
    os.symlink(f, t)


def read_md5_file(f):
    must_existed(f)
    o = {}
    find = re.compile('^(\w+)\s+(.*)')
    with open(f, 'r') as fd:
        s = fd.read()
    a = s.split("\n")
    for _a in a:
        _s = find.search(_a)
        if _s:
            o[_s.groups()[1]] = _s.groups()[0]
    return o


def main():
    must_existed(bin_location, True)
    links = arrange_node()
    latest = check_update()
    dir_name = get_version(latest['tag_name'])
    if dir_name is None:
        raise ValueError("Can not get version")
    dir_name = bin_location + "/" + dir_name
    if not is_existed(dir_name):
        print('Name: ' + latest['name'])
        # print('Tag: ' + latest['tag_name'])
        print('Create dir: ' + dir_name)
        os.mkdir(dir_name, 0o755)
        print('List download: ')
        for i, a in enumerate(latest['assets']):
            print('[%d] download %s to %s' % (i, a['name'], dir_name + "/" + a['name']))
            download(a['browser_download_url'], dir_name + "/" + a['name'])
        # check file
        print("md5 check")
        md5_file = read_md5_file(dir_name + '/md5sum.txt')
        for n in md5_file:
            print("check %s" % n)
            hash_md5 = md5()
            with open(dir_name + '/' + n, 'rb') as fd:
                for chunk in iter(lambda: fd.read(4096), b""):
                    hash_md5.update(chunk)
            assert hash_md5.hexdigest() == md5_file[n]

        # find last version
        last_ver = find_last()
        print("latest ver dir is %s" % last_ver)
        for n in links:
            print("remove link %s" % links[n])
            remove_link(links[n])
            new_link = bin_location + '/' + last_ver + '/' + n
            print("%s => %s" % (new_link, links[n]))
            make_link(new_link, links[n])


if __name__ == "__main__":
    main()
