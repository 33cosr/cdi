import json
import MySQLdb
import os
from common import constant
from contextlib import contextmanager


# use context manager to manage database connection resource
@contextmanager
def get_db_connector():
    with open(os.path.join(constant.config_path, 'database.json'), 'r') as f:
        db_config = json.load(f)
        db = MySQLdb.connect(**db_config)
        yield db
        db.close()


def get_table(table_name):
    with get_db_connector() as db:
        cur = db.cursor()
        if table_name == 'lkp_last_name':
            cur.execute("select value, if_common from lkp_last_name")
            data = {}
            for i in cur.fetchall():
                data[i[0]] = i[1]
        elif table_name == 'lkp_name_respected':
            cur.execute("select value from lkp_name_respected")
            data = [i[0] for i in cur.fetchall()]
        elif table_name == 'lkp_minority_name':
            cur.execute("select value from lkp_minority_name")
            data = [i[0] for i in cur.fetchall()]
        else:
            data = None
    return data


def get_meta(file_name):
    with get_db_connector() as db:
        cur = db.cursor()
        sql = "SELECT id, delimiter FROM (SELECT * FROM dataset, (SELECT '" + file_name + "' as current_file)\
         a WHERE current_file like file_pattern) a"
        cur.execute(sql)
        output = cur.fetchone()
        if output[1] == '\\t':
            delimiter = '\t'
        else:
            delimiter = output[1]
        if output:
            data = {'data_id': output[0], 'delimiter': delimiter, 'rule': {}}
        else:
            data = None

        # Get module names and function names
        if not data:
            raise Exception(file_name + ': file pattern not found')
        sql = "SELECT module_name, function_name FROM vw_dataset_rule WHERE dataset_id = " + \
              str(data['data_id']) + " order by sequence"
        print sql
        cur.execute(sql)
        for i in cur.fetchall():
            if i[0] in data['rule']:
                data['rule'][i[0]].append(i[1])
            else:
                data['rule'][i[0]] = [i[1]]
    return data


if __name__ == "__main__":
    get_db_connector()

