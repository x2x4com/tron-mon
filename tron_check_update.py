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
import os
import requests
# import json
import re

java_tron_release = "https://api.github.com/repos/tronprotocol/java-tron/releases"
bin_location = "/home/jacky/tron/update"


def check_update():
    resp = requests.get(java_tron_release)
    data = resp.json()
    return data[0]


def download(url):
    pass


def get_version(tag):
    reg_ver = re.compile('^\w+-v(.*)$')
    find_all = reg_ver.findall(tag)
    if len(find_all) > 0:
        return find_all[0]
    return None


def check_existed(d):
    return os.path.exists(bin_location + "/" + d)


def main():
    latest = check_update()
    dir_name = get_version(latest['tag_name'])
    if not check_existed(dir_name):

        print('Name: ' + latest['name'])
        print('Tag: ' + latest['tag_name'])
        print('Create: ' + dir_name)
        print('List download: ')

        for i, a in enumerate(latest['assets']):
            print('[%d]' % i)
            print('    name: ' + a['name'])
            print('    url:' + a['browser_download_url'])


if __name__ == "__main__":
    main()
