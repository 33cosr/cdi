# -*- coding: UTF-8 -*-
import libs


class BaseCleaner:
    def __init__(self, data_set, func_list):
        self.func_list = func_list
        self.data_set = data_set
        input_layout = libs.parameter.get_layout('input')
        output_layout = libs.parameter.get_layout('output')
        n = len(input_layout)
        self.sequence = input_layout['Input_Sequence_Number']
        self.first_name = input_layout['Input_First_Name']
        self.full_name = input_layout['Input_Full_Name']
        self.last_name = input_layout['Input_Last_Name']
        self.middle_name = input_layout['Input_Middle_Name']
        self.nick_name = input_layout['Input_Nick_Name']
        self.prefix_name = input_layout['Input_Name_Prefix']
        self.org = input_layout['Input_Org_Name']
        self.address1 = input_layout['Input_Address_Line_1']
        self.address2 = input_layout['Input_Address_Line_2']
        self.address3 = input_layout['Input_Address_Line_3']
        self.name_flag = output_layout['Name_Conf_flag'] + n


