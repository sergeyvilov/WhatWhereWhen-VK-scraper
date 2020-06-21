#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import vk_api

import mysql.connector

from get_post import get_post

from datetime import datetime

###get user data####
import json

with open('user_data.json') as f:
    user_data = json.load(f)

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

#######Open db########
print("Opening the local database...")
mydb = mysql.connector.connect(
    host = "localhost",
    user = user_data['sql_login'],
    passwd = user_data['sql_pswd'],
    database = "questions_chgk"
)

mycursor = mydb.cursor()
print("Database opened!")
mycursor.execute("SELECT COUNT(*) FROM questions_of_chgk")
print("Total questions in the local database: {}".format(mycursor.fetchone()[0]))
#####################

mycursor.execute("SELECT date  FROM questions_of_chgk ORDER BY date DESC LIMIT 1")
last_record = mycursor.fetchone()
if last_record == None:
    last_db_date = datetime.min
else:
    last_db_date = last_record[0]
    print("Latest question was posted on: {}\n".format(last_db_date))


print("Updating...")

first_post = vk.wall.get(count = 1, domain = 'questions_of_chgk')

posts_per_call = 100
total_posts = first_post['count']
#total_posts = 20

total_added = 0
post_number = 0

while post_number < total_posts:
    some_posts = vk.wall.get(count = posts_per_call, offset = post_number,
    domain = 'questions_of_chgk')
    pending_questions = []
    for c_post in range(posts_per_call):
        post_number += 1
        if post_number > total_posts:
            break
        c_question = get_post(some_posts['items'][c_post])
        if c_question != None:
            created_on = datetime.fromtimestamp(c_question['date'])
            if last_db_date < created_on:
                pending_questions.append(
                    (
                    c_question['id'],
                    created_on,
                    c_question['text'][0:1500],
                    c_question['answer'][0:1500],
                    c_question['poll']['yes'],
                    c_question['poll']['no'],
                    c_question['likes'],
                    c_question['views'],
                    0
                    )
                )
            else:
                post_number = total_posts
                break
    if pending_questions:
        sql = ("INSERT INTO questions_of_chgk"
          " (id, date, text, answer, yes, no, likes, views, solved)"
          " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        mycursor.executemany(sql, pending_questions)
        mydb.commit()
        total_added += mycursor.rowcount
        print("{} questions added, the earliest being posted on: {}".format(total_added, created_on))
    if post_number > total_posts:
        break

if not total_added:
    print("Local database is up to date!")
