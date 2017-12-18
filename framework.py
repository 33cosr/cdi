#!/usr/bin/python
# 20171218     init    Liang Hao
import MySQLdb
from os import listdir
from os.path import isfile, join

db = MySQLdb.connect(host="139.224.10.176",    # your host, usually localhost
                     user="hadoop",         # your username
                     passwd="mysql",  # your password
                     db="KB")        # name of the data base

cur = db.cursor()

# Get landing directory
cur.execute("SELECT value FROM parameter where name = 'LandingDir'")

landingDir = cur.fetchone()

# Get regular files under landing directory
fileList = [f for f in listdir(landingDir) if isfile(join(landingDir, f))]

# For each file get customer ID
fileCustomer = { }
for f in fileList:
    cur.execute("SELECT id FROM (SELECT * FROM customer, (SELECT '" + f + "' as current_file) a WHERE current_file like 'file_name'")
    if id:
        fileCustomer[f] = {'customer_id': id}

# Get rules
for f in fileCustomer:
    cur.execute("SELECT rule_id, step_id FROM customer_rule WHERE customer_id = " + fileCustomer[f]['customer_id'])
    fileCustomer[f]['customer_id'] = cur.fetchall()


db.close()