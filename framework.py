#!/usr/bin/python
# 20171218     init    Liang Hao
import cleaner
import MySQLdb
from os import listdir
from os.path import isfile, join


def file_to_array(path):
    with open(path, 'r') as f:
        lines = f.read()
    if lines[-1] == '\n':
        lines = lines[: -1]
    return lines.split('\n')


def array_to_file(path, data, delimiter):
    with open(path, 'w') as f:
        for line in data:
            for field in line[:-1]:
                f.write(field + delimiter)
            f.write(line[-1] + '\n')


db = MySQLdb.connect(host="192.168.77.4", user="hadoop", passwd="mysql", db="KB")

cur = db.cursor()

# Get landing directory and staging directory
cur.execute("SELECT value FROM parameter where name = 'LandingDir'")

landing_dir = cur.fetchone()[0]

cur.execute("SELECT value FROM parameter where name = 'StagingDir'")

staging_dir = cur.fetchone()[0]

cur.execute("SELECT value FROM parameter where name = 'ArchiveDir'")

archive_dir = cur.fetchone()[0]

# Get regular files under landing directory
file_list = [f for f in listdir(landing_dir) if isfile(join(landing_dir, f))]

# For each file get Dataset ID
file_data = {}
for f in file_list:
    sql = "SELECT id, delimiter FROM (SELECT * FROM dataset, (SELECT '" + f + "' as current_file) a WHERE current_file like file_pattern) a"
    print sql
    cur.execute(sql)
    output = cur.fetchone()
    if output[1] == '\\t':
        delimiter = '\t'
    else:
        delimiter = output[1]
    if output:
        file_data[f] = {'data_id': output[0], 'delimiter': delimiter, 'rule': {}}

# Get module names and function names
for f in file_data:
    sql = "SELECT module_name, function_name FROM vw_dataset_rule WHERE dataset_id = " + str(file_data[f]['data_id']) + " order by sequence"
    print sql
    cur.execute(sql)
    for i in cur.fetchall():
        if i[0] in file_data[f]['rule']:
            file_data[f]['rule'][i[0]].append(i[1])
        else:
            file_data[f]['rule'][i[0]] = [i[1]]

print file_data

# Check layout and rules
for f in file_data:
    data_set = file_to_array(join(landing_dir, f))
    data_set = [line.split(file_data[f]['delimiter']) for line in data_set]
    # cur.execute("SELECT field_sequence, field_name FROM file_layout WHERE dataset_id = " + str(file_data[f]['data_id']) + " order by field_sequence")
    # layout = cur.fetchall()
    # print layout
    # print data_set
    # header = data_set[0]
    # layout_valid = True
    # for sequence in range(len(header)):
    #     if sequence >= len(layout) or sequence + 1 != layout[sequence][0] or header[sequence] != layout[sequence][1]:
    #         layout_valid = False
    #         break
    # if not layout_valid:
    #     print f + 'layout is not valid'
    #     continue
    cleaner.clean(data_set, file_data[f])
    print 'after clean'
    print data_set
    array_to_file(join(staging_dir, f), data_set, file_data[f]['delimiter'])
    # Move to archive
    # os.rename(join(landing_dir, f), join(archive_dir, f))

db.close()

print file_data







