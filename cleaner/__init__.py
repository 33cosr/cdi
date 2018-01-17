import importlib
from cleaner import *
import libs


def clean(data_set, meta):
    output_layout = libs.parameter.get_layout('output')
    n = len(data_set[0])
    for record in data_set:
        record += [u'' for i in output_layout]
    for f in output_layout:
        data_set[0][n + output_layout[f]] = f
    for mod, func in meta['rule'].iteritems():
        rule_module = importlib.import_module('cleaner.' + mod)
        cleaner = rule_module.Cleaner(data_set=data_set, func_list=func)
        cleaner.clean()


