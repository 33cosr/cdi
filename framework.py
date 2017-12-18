#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host="139.224.10.176",    # your host, usually localhost
                     user="hadoop",         # your username
                     passwd="mysql",  # your password
                     db="KB")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM YOUR_TABLE_NAME")

# print all the first cell of all the rows
for row in cur.fetchall():
    print row[0]

db.close()