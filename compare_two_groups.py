#!/usr/bin/env python
# -*- coding: utf-8 -*-:wq
import vk_api

import mysql.connector

from get_post import get_post

from datetime import datetime

###get user data####
import json

with open('user_data.json') as f:
    user_data = json.load(f)
####

#######Connect to vk#########
print("Connecting to VK...")

login, password = user_data['vk_login'], user_data['vk_pswd']
vk_session = vk_api.VkApi(login, password)

try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
    quit()

vk = vk_session.get_api()
print('Successfully connected!\n')


members_per_call = 1000
total_members = vk.groups.getMembers(count = 1, offset = 0, group_id = 'questions_of_chgk')
total_members = total_members['count']

members_qu_of_ch = []
for offset in range(0, total_members, members_per_call):
    members = vk.groups.getMembers(count = members_per_call, offset = \
    offset, group_id = 'questions_of_chgk')
    members_qu_of_ch.extend(members['items'])
#    print(members_qu_of_ch)
#    quit()
    #print(members['items'])
    #is_member = vk.groups.isMember(group_id = 'baza_chto_gde_kogda',users_ids = \
    #{1, 2})
    #print(is_member)
    #print('Number of intersections:'.format(sum(is_member)))
    print("questions_of_chgk: {} members added".format(len(members_qu_of_ch)))

total_members = vk.groups.getMembers(count = 1, offset = 0, group_id = 'baza_chto_gde_kogda')
total_members = total_members['count']

members_baza = []
for offset in range(0, total_members, members_per_call):
    members = vk.groups.getMembers(count = members_per_call, offset = \
    offset, group_id = 'baza_chto_gde_kogda')
    members_baza.extend(members['items'])
    print("baza_chto_gde_kogda: {} members added".format(len(members_baza)))

print('{} members are the same in the two groups'.format(len(list(set(members_qu_of_ch) & set(members_baza)))))
