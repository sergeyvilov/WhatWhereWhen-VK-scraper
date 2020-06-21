#!/usr/bin/env python
# -*- coding: utf-8 -*-:wq

import mysql.connector
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
import matplotlib.pyplot as plt
from operator import truediv
import math

###get user data####
import json

with open('user_data.json') as f:
    user_data = json.load(f)
####

def get_median(sql_cursor, total_rows, column_name, where_statement):
    sql = "SELECT MAX(" + column_name + ") FROM questions_of_chgk WHERE " + where_statement +\
    " ORDER BY " + column_name + " LIMIT " + str(int(math.floor(total_rows/2)))
    sql_cursor.execute(sql)
    median = int(sql_cursor.fetchone()[0])
    if not total_rows % 2:
        sql = "SELECT MAX(" + column_name + ") FROM questions_of_chgk WHERE " +\
        where_statement + " ORDER BY " + column_name + " LIMIT " + \
        str(int(math.floor(total_rows/2 + 1)))
        sql_cursor.execute(sql)
        median += int(sql_cursor.fetchone()[0])
        median = median / 2.0
    return median

mydb = mysql.connector.connect(
    host = "localhost",
    user = user_data['sql_login'],
    passwd = user_data['sql_pswd'],
    database = "questions_chgk"
)

mycursor = mydb.cursor()

sql = "SELECT COUNT(*) FROM questions_of_chgk"
mycursor.execute(sql)
print(u"Всего в базе {} вопросов".format(mycursor.fetchone()[0]))


sql = "SELECT COUNT(*) FROM questions_of_chgk" +\
" WHERE DATEDIFF(NOW(), date) < 180"
mycursor.execute(sql)
questions_per_day = round(int(mycursor.fetchone()[0])/(180.0))
print(u"В день публикуются {} вопросов".format(questions_per_day))

isnotnull = " WHERE yes + no > 384"

sql = "SELECT COUNT(*) FROM questions_of_chgk" + isnotnull
mycursor.execute(sql)
total_questions_of_chgk = mycursor.fetchone()[0]
print(u"Данные опросов имеются для {} вопросов".format(total_questions_of_chgk))



distr = []
sql = "SELECT date FROM questions_of_chgk" + isnotnull +\
 " ORDER BY date LIMIT 1"
mycursor.execute(sql)
earliest = mycursor.fetchone()[0]
sql = "SELECT date FROM questions_of_chgk" + isnotnull + " ORDER BY date DESC LIMIT 1"
mycursor.execute(sql)
latest = mycursor.fetchone()[0]
print(u"Самый ранний вопрос опубликован {}\nСамый поздний вопрос опубликован {}".format(earliest,latest))

for frame in range(0, 100, 10):
    low = (frame + 0.) / 100
    high = (frame + 10.) / 100
    sql = "SELECT COUNT(*) FROM questions_of_chgk WHERE yes/(yes+no)>=" + str(low) + \
    " AND yes/(yes+no)<" + str(high)
    mycursor.execute(sql)
    distr.append(mycursor.fetchone()[0])

#sql = "SELECT date, views FROM questions_of_chgk WHERE views IS NOT NULL ORDER BY date"
#sql = "SELECT MONTH(date), AVG(views) FROM questions_of_chgk GROUP BY MONTH(date)"
#mycursor.execute(sql)
#dates, views = zip(*mycursor.fetchall())
#print(zip(dates,views))

likes = []
likes_std = []
for frame in range(0, 100, 10):
    low = (frame + 0.) / 100
    high = (frame + 10.) / 100
#    sql = "SELECT AVG(likes) FROM questions_of_chgk WHERE yes/(yes+no)>=" + str(low) + \
#    " AND yes/(yes+no)<" + str(high)
#    mycursor.execute(sql)
#    likes.append(mycursor.fetchone()[0])
#    sql = "SELECT STD(likes) FROM questions_of_chgk WHERE yes/(yes+no)>=" + str(low) + \
#    " AND yes/(yes+no)<" + str(high)
#    mycursor.execute(sql)
#    likes_std.append(mycursor.fetchone()[0])
    total_rows = distr[frame / 10]
    where_statement = "yes/(yes+no)>=" + str(low) + " AND yes/(yes+no)<" +\
    str(high)
    likes.append(get_median(mycursor, total_rows, 'likes', where_statement ))

#######################
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_style = LS('#333366', base_style = LCS)
my_style.title_font_size = 24
my_style.label_font_size = 20
my_style.major_label_font_size = 20
my_style.tooltip_font_size = 20

#my_config = pygal.Config()
#my_config.x_label_rotation = 45

hist = pygal.Bar(my_config, style = my_style)
hist.title = u'Распределение вопросов по сложности'
hist.x_labels = ['0-10%','10%-20%','20%-30%','30%-40%','40%-50%','50%-60%','60%-70%','70%-80%','80%-90%','90%-100%']
hist.x_title = u"Доля ответивших на вопрос (согласно результатам опросов)"
hist.y_title = u"Количество вопросов"
#hist.show_legend = False

hist.add('',distr)
hist.render_to_file('difficulty_level.svg')
########################
hist = pygal.Bar(my_config, style = my_style)
hist.title = u'Распределение лайков в зависимости от сложности вопросов'
hist.x_labels = ['0-10%','10%-20%','20%-30%','30%-40%','40%-50%','50%-60%','60%-70%','70%-80%','80%-90%','90%-100%']
hist.x_title = u"Доля ответивших на вопрос (согласно результатам опросов)"
hist.y_title = u"Количество лайков на один вопрос (медианное значение)"
#hist.show_legend = False

#hist.add('',map(round,map(truediv,likes, distr)))
hist.add('',likes)
#hist.add('', [round((a+b)/(2.0)) for a,b in zip(likes[0:10:2], likes[1:10:2])])
hist.render_to_file('likes_vs_difficulty.svg')
