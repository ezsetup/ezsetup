import json
from typing import List, Tuple, Dict, Any

import yaml
from jinja2 import FileSystemLoader, Environment


template_loader = FileSystemLoader("cloudops/configurations")
template_environment = Environment(loader=template_loader)

def generate_userdata(configurations: List[Dict[str, Any]]) -> str:
    """ generate cloudinit userdata from a list of configurations
    Return userdata"""
    with open('cloudops/configurations/templates.json') as f:
        templates = json.load(f)

    userdata = None
    for conf in configurations:
        path = _get_template_path(templates, conf['name'])
        with open('cloudops/configurations/' + path) as f:
            template = template_environment.get_template(path)
            rendered = template.render(conf['params'])
            yaml_loaded_obj = yaml.load(rendered) 
            userdata = _merge_user_data(userdata, yaml_loaded_obj) 
    return "#cloud-config\n" + yaml.dump(userdata)

def _get_template_path(templates, name: str) -> str:
    for template in templates:
        if template['name'] == name:
            return template['path']
    raise ValueError('invalid `name` parameter. It should be one of the names defined in templates.json')

def _merge_user_data(old_user_data, new_user_data) -> Dict:
    if old_user_data is None:
        """Nothing to merge"""
        old_user_data = new_user_data
    else:
        for key in new_user_data:
            if key in old_user_data:
                if isinstance(old_user_data[key], list):
                """Merge two values of two same key"""
                    if isinstance(new_user_data[key], list):
                        old_user_data[key].extend(new_user_data[key])
                    else:
                        old_user_data[key].append(new_user_data[key])
                else:
                    old_user_data[key]=new_user_data[key]
            else:
                old_user_data[key] = new_user_data[key]
    return old_user_data
