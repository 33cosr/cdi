# -*- coding: UTF-8 -*-
import re
import clean_utility
import libs
import clean


class Cleaner(clean.BaseCleaner):
    def __init__(self, data_set, func_list):
        clean.BaseCleaner.__init__(self, data_set, func_list)
        self.last_name_list = {}
        data = libs.db_connector.get_table('lkp_last_name', 'value', 'most_common_flag')
        for i in data:
            self.last_name_list[i[0]] = i[1]
        self.name_respected_list = [i[0] for i in libs.db_connector.get_table('lkp_name_respected')]
        self.name_list = [self.first_name, self.last_name, self.full_name, self.middle_name]
        self.minority_name_list = [i[0] for i in libs.db_connector.get_table('lkp_minority_name')]
        self.vulgar_name_list = [i[0] for i in libs.db_connector.get_table('lkp_vulgar_name')]

    def clean(self):
        for i in range(1, len(self.data_set)):
            for f in self.func_list:
                getattr(self, f)(self.data_set[i])

    def remove_special_character(self, record):
        for i in self.name_list:
            # print value, record
            record[i] = re.sub(r"[0-9_]", '', re.sub(r"[\W]+", "", record[i], flags=re.UNICODE), flags=re.UNICODE)

    def full2half(self, record):
        for i in self.name_list:
            record[i] = clean_utility.unicode_string.stringQ2B(record[i])

    def trim(self, record):
        for i in self.name_list:
            record[i] = record[i].strip()

    def remove_all_whitespace(self, record):
        for i in self.name_list:
            record[i] = u''.join(record[i].split())

    def remove_alphabet(self, record):
        for i in self.name_list:
            record[i] = u''.join([uchar for uchar in record[i] if not clean_utility.unicode_string.is_alpha(uchar)])

    def filter_vulgar_list(self, record):
        for i in self.name_list:
            if record[i] in self.vulgar_name_list:
                record[i] = u''

    def org_name2name(self, record):
        self.other2name(record, [self.org])

    def address2name(self, record):
        self.other2name(record, [self.address1, self.address2, self.address3])

    def nick_name2name(self, record):
        self.other2name(record, [self.nick_name])

    def other2name(self, record, field_list):
        for i in self.name_list:
            if record[i]:
                return
        for i in field_list:
            val = record[i].strip()
            if len(val) in [2, 3] and val[0] in self.last_name_list:
                record[self.full_name] = val
                record[i] = u''
                return

    def other2prefix(self, record, field_list):
        if record[self.prefix_name]:
            return
        for i in field_list:
            val = record[i].strip()
            for name in self.name_respected_list:
                if name in val:
                    val.replace(name, '')
                    record[self.prefix_name] = name
                    break

    def full2prefix(self, record):
        self.other2prefix(record, [self.full_name])

    def last2prefix(self, record):
        self.other2prefix(record, [self.last_name])

    def first2prefix(self, record):
        self.other2prefix(record, [self.first_name])

    def populate_full_name(self, record):
        if not record[self.full_name] and record[self.last_name]\
                and record[self.first_name]:
            record[self.full_name] = record[self.last_name] + record[self.first_name]

    def other2full(self, record):
        if record[self.first_name] and record[self.last_name] and record[self.middle_name]:
            return
        if not record[self.full_name]:
            if record[self.middle_name]:
                if not record[self.last_name]:
                    record[self.last_name] = record[self.middle_name]
                else:
                    record[self.last_name] = record[self.middle_name]
                record[self.middle_name] = u''
            else:
                if not record[self.last_name]:
                    record[self.last_name] = record[self.first_name]
                    record[self.first_name] = u''
            record[self.full_name] = record[self.first_name] + record[self.last_name]

    def full2other(self, record):
        if record[self.full_name] and len(record[self.full_name]) < 5 and not record[self.last_name] \
                and not record[self.first_name]:
            if record[self.full_name][:2] in self.last_name_list:
                record[self.first_name] = record[self.full_name][2:]
                record[self.last_name] = record[self.full_name][:2]
            else:
                record[self.first_name] = record[self.full_name][1:]
                record[self.last_name] = record[self.full_name][:1]

    def full2first(self, record):
        if record[self.full_name] and len(record[self.full_name]) < 5 and \
                        record[self.last_name] == record[self.full_name] and not record[self.first_name]:
            if record[self.full_name][:2] in self.last_name_list:
                record[self.first_name] = record[self.full_name][2:]
                record[self.last_name] = record[self.full_name][:2]
            else:
                record[self.first_name] = record[self.full_name][1:]
                record[self.last_name] = record[self.full_name][:1]

    def full2last(self, record):
        if record[self.full_name] and len(record[self.full_name]) < 5 and \
                        record[self.first_name] == record[self.full_name] and not record[self.last_name]:
            if record[self.full_name][:2] in self.last_name_list:
                record[self.first_name] = record[self.full_name][2:]
                record[self.last_name] = record[self.full_name][:2]
            else:
                record[self.first_name] = record[self.full_name][1:]
                record[self.last_name] = record[self.full_name][:1]

    def update_full(self, record):
        if record[self.full_name] and len(record[self.full_name]) < 5 and \
                        record[self.full_name] != record[self.last_name] + record[self.first_name] and \
                        record[self.full_name] == record[self.first_name] + record[self.last_name] and \
                        record[self.last_name] in self.last_name_list and record[self.first_name] not in self.last_name_list:
            record[self.full_name] = record[self.last_name] + record[self.first_name]

    def swap_first_last(self, record):
        if record[self.full_name] and len(record[self.full_name]) < 5 and \
                        record[self.full_name] != record[self.last_name] + record[self.first_name] and \
                        record[self.full_name] == record[self.first_name] + record[self.last_name] and \
                        record[self.first_name] in self.last_name_list and len(record[self.first_name]) == 1 and \
                        record[self.last_name] not in self.last_name_list:
            temp = record[self.first_name]
            record[self.first_name] = record[self.last_name]
            record[self.last_name] = temp

    def dedup_last_4(self, record):
        if record[self.full_name] and len(record[self.full_name]) == 4 and \
                record[self.full_name] == record[self.last_name] + record[self.first_name] and \
                record[self.full_name][0] == record[self.full_name][1] and record[self.full_name][0] in self.last_name_list:
            record[self.last_name] = record[self.full_name].pop(0)
            record[self.first_name] = record[self.full_name][1:]

    def dedup_last_3(self, record):
        if record[self.full_name] and len(record[self.full_name]) == 3 and \
                record[self.full_name] == record[self.last_name] + record[self.first_name] and \
                record[self.full_name][0] == record[self.full_name][1] and record[self.full_name][0] in self.last_name_list:
            record[self.last_name] = record[self.full_name].pop(0)
            record[self.first_name] = record[self.full_name][1:]

    def update_flag_1(self, record):
        full_name = record[self.full_name]
        if len(full_name) == 3 and full_name[0] in self.last_name_list and self.last_name_list[full_name[0]] == 'Y':
            record[self.name_flag] = 1

    def update_flag_2(self, record):
        full_name = record[self.full_name]
        if len(full_name) == 2 and full_name[0] in self.last_name_list and self.last_name_list[full_name[0]] == 'Y':
            record[self.name_flag] = 1

    def update_flag_3(self, record):
        full_name = record[self.full_name]
        if len(full_name) == 3 and full_name[:2] in self.last_name_list:
            record[self.name_flag] = 1

    def update_flag_4(self, record):
        full_name = record[self.full_name]
        if len(full_name) == 4 and full_name[:2] in self.last_name_list:
            record[self.name_flag] = 1

    def update_flag_5(self, record):
        full_name = record[self.full_name]
        if len(full_name) == 3 and full_name[0] in self.last_name_list and self.last_name_list[full_name[0]] != 'Y':
            record[self.name_flag] = 2

    def update_flag_6(self, record):
        full_name = record[self.full_name]
        if len(full_name) == 2 and full_name[0] in self.last_name_list and self.last_name_list[full_name[0]] != 'Y':
            record[self.name_flag] = 2

    def update_flag_7(self, record):
        full_name = record[self.full_name]
        if len(full_name) == 3 and full_name[0] not in self.last_name_list:
            record[self.name_flag] = 3

    def update_flag_8(self, record):
        full_name = record[self.full_name]
        if len(full_name) == 2 and full_name[0] not in self.last_name_list:
            record[self.name_flag] = 3

    def update_flag_9(self, record):
        full_name = record[self.full_name]
        if len(full_name) == 2 and full_name[:2] in self.last_name_list:
            record[self.name_flag] = 4

    def update_flag_10(self, record):
        full_name = record[self.full_name]
        if len(full_name) == 1 and full_name[0] in self.last_name_list:
            record[self.name_flag] = 4

    def update_flag_11(self, record):
        full_name = record[self.full_name]
        if len(full_name) > 3 and full_name in self.minority_name_list:
            record[self.name_flag] = 5

    def update_flag_12(self, record):
        full_name = record[self.full_name]
        if len(full_name) > 3 and clean_utility.unicode_string.is_all_alpha(full_name):
            record[self.name_flag] = 6

    def update_flag_13(self, record):
        full_name = record[self.full_name]
        if len(full_name) > 3 and full_name[0] in self.last_name_list and self.last_name_list[full_name[0]] == 'Y' \
                and full_name[1] in self.last_name_list and self.last_name_list[full_name[1]] == 'Y':
            record[self.name_flag] = 7

    def update_flag_14(self, record):
        full_name = record[self.full_name]
        if len(full_name) > 3 and full_name[0] in self.last_name_list and self.last_name_list[full_name[0]] == 'Y' \
                and full_name[3] in self.last_name_list and self.last_name_list[full_name[3]] == 'Y':
            record[self.name_flag] = 7

    def update_flag_15(self, record):
        full_name = record[self.full_name]
        if len(full_name) > 3 and not record[self.name_flag]:
            record[self.name_flag] = 8

    def update_flag_16(self, record):
        if not record[self.name_flag]:
            record[self.name_flag] = 9


if __name__ == "__main__":
    # s = unicode('郝亮  ,66', 'utf-8')
    # print re.sub(r"[0-9_]", '', re.sub(r"[\W]+", "", s, flags=re.UNICODE))
    a = Cleaner([['first name', 'last name'], [u'全椒', u'  hao 好 laing  ']], ['remove_alphabet'])
    print a.data_set
    a.clean()
    print a.data_set[1][0]
    print a.data_set

