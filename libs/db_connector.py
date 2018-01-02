# -*- coding: UTF-8 -*-
import json
import MySQLdb
import os
import constant
from contextlib import contextmanager


# use context manager to manage database connection resource
@contextmanager
def get_db_connector():
    with open(os.path.join(constant.config_path, 'database.json'), 'r') as f:
        db_config = json.load(f)
        db = MySQLdb.connect(**db_config)
        yield db
        db.close()


def get_table(table_name, *column):
    if column is None:
        column = ['value']
    with get_db_connector() as db:
        cur = db.cursor()
        sql = "select "
        for f in column:
            sql += f + ","
        sql[-1] = " "
        sql += "from " + table_name
        cur.execute(sql)
        return cur.fetchall()


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


def insert_last_name():
    s = u"赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏\
水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬\
安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜\
阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁锺徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪\
干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄麴家封芮羿储靳汲邴糜\
松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭历戎祖武符刘景詹束龙叶幸\
司韶郜黎蓟溥印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阳郁胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉\
宰郦雍却璩桑桂濮牛寿通边扈燕冀僪浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终\
暨居衡步都耿满弘匡国文寇广禄阙东欧殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙\
乜养鞠须丰巢关蒯相查后荆红游竺权逮盍益桓公朴付肖钟闫沐曲邝商岳"
    s1 = u"欧阳,太史,端木,上官,司马,独孤,南宫,夏侯,诸葛,尉迟,公羊,赫连,澹台,皇甫,公孙,慕容,长孙,宇文,司徒,鲜于,司空,拓跋,轩辕,令狐,段干,百里,呼延,东郭,南门"
    sql = u"insert into lkp_last_name(value) values"
    for i in s:
        sql += u"('" + i + u"'),"
    s1 = s1.split(u',')
    for i in s1:
        sql += u"('" + i + u"'),"
    sql = sql[:-1]
    sql = sql.encode('utf8')
    print sql
    with get_db_connector() as db:
        cur = db.cursor()
        cur.execute(sql)


if __name__ == "__main__":
    pass

