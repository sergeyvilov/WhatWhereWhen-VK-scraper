#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector
import sys

###get user data####
import json

with open('user_data.json') as f:
    user_data = json.load(f)
####

if len(sys.argv) > 2:
    low = sys.argv[1]
    high = sys.argv[2]
else:
    low = '0'
    high = '1'

mydb = mysql.connector.connect(
    host = "localhost",
    user = user_data['sql_login'],
    passwd = user_data['sql_pswd'],
    database = "questions_chgk"
)

mycursor = mydb.cursor()

sql = "SELECT COUNT(*) FROM questions_of_chgk WHERE yes/(yes+no)>" + low + \
" AND yes/(yes+no)<" + high + " AND solved = 0"
mycursor.execute(sql)
print(u"Выбираем из {} вопросов\n".format(mycursor.fetchone()[0]))

sql = "SELECT * FROM questions_of_chgk WHERE yes/(yes+no)>" + low + \
" AND yes/(yes+no)<" + high + " AND solved = 0 ORDER BY RAND() LIMIT 1"
mycursor.execute(sql)
questions = mycursor.fetchall()


for i in range(len(questions)):
   print(u"Вопрос {} опубликован {}\n".format(questions[i][0], questions[i][1]))
   print(u"{}\n".format(questions[i][2]))
   print(u"Ответили:{} Не ответили:{} Likes:{} Views: {}\n".format(questions[i][4], questions[i][5], questions[i][6], questions[i][7]))
   r = input(u"Press Ctrl+C to exit, any other key for the answer\n")
   print(questions[i][3])
   sql = "UPDATE questions_of_chgk SET solved = 1 WHERE id = " + str(questions[i][0])
#   print(sql)
   mycursor.execute(sql)
   mydb.commit()

if not questions:
    print('Вы прорешали все вопросы данной категории!')
