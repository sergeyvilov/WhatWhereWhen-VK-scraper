#!/usr/bin/env python3
import mysql.connector

print('If you continue, the questions database will be'
'completely deleted if it already exists!\n'
'Press Ctrl+C to exit, Enter to continue')
input()

###get user data####
import json

with open('user_data.json') as f:
    user_data = json.load(f)
####

mydb = mysql.connector.connect(
    host = "localhost",
    user = user_data['sql_login'],
    passwd = user_data['sql_pswd']
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS questions_chgk")

mycursor.execute("USE questions_chgk")

#mycursor.execute("ALTER TABLE questions_of_chgk MODIFY COLUMN solved TINYINT(1)")
#mycursor.execute("UPDATE questions_of_chgk SET solved = 0")
#mycursor.execute("ALTER TABLE baza_chto_gde_kogda MODIFY COLUMN solved TINYINT(1)")
#mycursor.execute("UPDATE baza_chto_gde_kogda SET solved = 0")

mycursor.execute("DROP TABLE IF EXISTS questions_of_chgk")

mycursor.execute("CREATE TABLE questions_of_chgk (id MEDIUMINT, date DATETIME,"+
"text VARCHAR(1500), answer VARCHAR(1500), yes MEDIUMINT UNSIGNED, " +
"no MEDIUMINT UNSIGNED, likes MEDIUMINT UNSIGNED, views MEDIUMINT UNSIGNED, " +
"solved BOOLEAN) CHARACTER SET utf8mb4")

print('Empty database is successfully created.')
