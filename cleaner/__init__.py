import importlib
from cleaner import *


def clean(data_set, meta):
    for module in meta['rule']:
        rule_module = importlib.import_module('cleaner.' + module)
        cleaner = rule_module.Cleaner(data_set)
        for func in meta['rule'][module]:
            getattr(cleaner, func)()


