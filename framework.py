#!/usr/bin/python
# 20171218     init    Liang Hao
import cleaner
import os
import libs

# Get landing directory and staging directory
para = libs.parameter.Parameter()

# Get regular files under landing directory
file_list = [f for f in os.listdir(para.landing_dir) if os.path.isfile(os.path.join(para.landing_dir, f))]

# For each file get meta data
file_data = {}
for f in file_list:
    file_data[f] = libs.db_connector.get_meta(f)

print file_data

# Check rules
for f in file_data:
    data_set = libs.utility.file_to_array(os.path.join(para.landing_dir, f))
    data_set = [line.split(file_data[f]['delimiter']) for line in data_set]
    cleaner.clean(data_set, file_data[f])
    print 'after clean'
    print data_set
    libs.utility.array_to_file(os.path.join(para.staging_dir, f), data_set, file_data[f]['delimiter'])
    # Move to archive
    # os.rename(join(landing_dir, f), join(archive_dir, f))

print file_data







