# -*- coding: UTF-8 -*-
import re
import clean_utility
import libs
import clean
from collections import OrderedDict


class Cleaner(clean.BaseCleaner):
    def __init__(self, data_set, func_list):
        clean.BaseCleaner.__init__(self, data_set, func_list)
        self.email_list = [self.email_address1, self.email_address2]
        self.vulgar_email_list = [i[0] for i in libs.db_connector.get_table('lkp_vulgar_email')]
        self.pattern = re.compile(r'([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]')
        self.valid1 = False
        self.valid2 = False

    def clean(self):
        for i in range(1, len(self.data_set)):
            record = self.data_set[i]
            if self.pattern.match(record[self.email_address1]):
                self.valid1 = True
            if self.pattern.match(record[self.email_address2]):
                self.valid2 = True
            for f in self.func_list:
                getattr(self, f)(self.data_set[i])

    # 1-1
    def remove_mess(self, record):
        for i in self.email_list:
            s = u''
            for j in record[i]:
                if 32 <= ord(j) < 127:
                    s += j
            record[i] = s

    # 1-2
    def full2half(self, record):
        for i in self.email_list:
            record[i] = clean_utility.unicode_string.stringQ2B(record[i])

    # 1-3
    def trim(self, record):
        for i in self.email_list:
            record[i] = record[i].strip()

    # 2-1
    def filter_vulgar_list(self, record):
        for i in self.email_list:
            if record[i] in self.vulgar_email_list:
                record[i] = u''

    # 3-1
    def deduplicate(self, record):
        if record[self.email_address1] and record[self.email_address2] == record[self.email_address1]:
            record[self.email_address2] = u''

    # 3-2
    def email2to1(self, record):
        if not record[self.email_address1] and record[self.email_address2]:
            record[self.email_address1] = record[self.email_address2]

    def other2email(self, record, field_list):
        if not record[self.email_address1] and not record[self.email_address2]:
            if not self.valid1 and not self.valid2:
                val_list = [record[i] for i in field_list]
                val_list = list(OrderedDict.fromkeys(val_list))
                email_list = [i for i in val_list if self.pattern.match(i)]
                n = len(email_list)
                if n == 1:
                    record[self.email_address1] = email_list[0]
                elif n >= 2:
                    record[self.email_address1] = email_list[0]
                    record[self.email_address2] = email_list[1]

    # 3-3
    def address2email(self, record):
        self.other2email(record, [self.address1, self.address2, self.address3])

    # 3-4
    def phone2email(self, record):
        self.other2email(record, [self.phone1, self.phone2, self.phone2])

    # 3-5
    def org2email(self, record):
        self.other2email(record, [self.org])

    # 3-6
    def name2email(self, record):
        self.other2email(record, [self.full_name])

    # 3-6
    def qq2email(self, record):
        if not record[self.email_address1] and not record[self.email_address2]:
            if not self.valid1 and not self.valid2:
                if re.match('[1-9][0-9]{4, 11}', record[self.qq]):
                    record[self.email_address1] = record[self.qq] + '@qq.com'

    # 4-1
    def update_flag1(self, record):
        if not record[self.email_address1]:
            record[self.email1_flag] = 'B'
        if not record[self.email_address2]:
            record[self.email2_flag] = 'B'

    # 4-2
    def update_flag2(self, record):
        if self.valid1:
            record[self.email1_flag] = 'Y'
        if self.valid2:
            record[self.email2_flag] = 'Y'

    # 4-3
    def update_flag3(self, record):
        if not self.valid1:
            record[self.email1_flag] = 'N'
        if not self.valid2:
            record[self.email2_flag] = 'N'

    # 4-4
    def update_flag4(self, record):
        if not record[self.email1_flag]:
            record[self.email1_flag] = 'U'
        if not record[self.email2_flag]:
            record[self.email2_flag] = 'U'




