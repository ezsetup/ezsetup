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

def _merge_user_data(userdata, new_data) -> Dict:
    if userdata is None:
        userdata = new_data
    else:
        for k in new_data:
            if k in userdata:
                if isinstance(userdata[k], list):
                    if isinstance(new_data[k], list):
                        userdata[k].extend(new_data[k])
                    else:
                        userdata[k].append(new_data[k])
                else:
                    userdata[k]=new_data[k]
            else:
                userdata[k] = new_data[k]
    return userdata
