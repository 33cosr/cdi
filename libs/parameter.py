import json
import os
from libs import constant


class Parameter:
    def __init__(self):
        with open(os.path.join(constant.config_path, 'parameter.json'), 'r') as f:
            p = json.load(f)
        self.landing_dir = os.path.join(p['base'], p['landing'])
        self.staging_dir = os.path.join(p['base'], p['staging'])
        self.archive_dir = os.path.join(p['base'], p['archive'])


def get_dir():
    with open(os.path.join(constant.config_path, 'parameter.json'), 'r') as f:
        return json.load(f)


def get_layout(layout_name):
    with open(os.path.join(constant.config_path, 'layout.json'), 'r') as f:
        data = json.load(f)
        if layout_name == 'input':
            data = data['input']
        else:
            data = data['output']
        layout = {}
        for c, value in enumerate(data):
            layout[value] = c
    return layout
