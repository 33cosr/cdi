import importlib
from cleaner import *
import libs


def clean(data_set, meta):
    for record in data_set:
        record += [u'' for i in libs.parameter.get_layout('output')]
    for mod, func in meta['rule'].iteritems():
        rule_module = importlib.import_module('cleaner.' + mod)
        cleaner = rule_module.Cleaner(data_set=data_set, func_list=func)
        cleaner.clean()


