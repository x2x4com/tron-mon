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
import re

java_tron_release = "https://api.github.com/repos/tronprotocol/java-tron/releases"

resp = requests.get(java_tron_release)

data = resp.json()
latest = data[0]
dir_name = ""
reg_ver = re.compile('^\w+-v(.*)$')
find_all = reg_ver.findall(latest['tag_name'])

if len(find_all) > 0:
    dir_name = find_all[0]

print('Name: ' + latest['name'])
print('Tag: ' + latest['tag_name'])
print('Create: ' + dir_name)
print('List download: ')

for i, a in enumerate(latest['assets']):
    print('[%d]' % i)
    print('    name: ' + a['name'])
    print('    url:' + a['browser_download_url'])

