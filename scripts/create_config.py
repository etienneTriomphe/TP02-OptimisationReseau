import json
from jinja2 import Template, Environment, FileSystemLoader

def load_json_data_from_file(file_path):
    try:
        with open(file_path) as f:
            data = json.load(f)
            f.close()
    
    except IOError:
        print("Could not read file:", file_path)

    return data


def render_network_config(template_name, data):
    template = env.get_template(template_name) 
    return template.render(data) 


def save_built_config(file_name, data):
    try:
        with open(file_name, "w") as f:
            f.write(data)
            f.close()
    
    except IOError:
        print("Could not read file:", file_name)

def create_vlan_config_cpe_marseille():
    r02_config = render_network_config("vlan_router.j2",load_json_data_from_file("./data/vlan_R02.json"))
    esw2_config = render_network_config("vlan_switch.j2",load_json_data_from_file("./data/vlan_ESW2.json"))
    return r02_config, esw2_config

def create_vlan_config_cpe_paris():
    r03_config = render_network_config("vlan_router.j2",load_json_data_from_file("./data/vlan_R03.json"))
    esw3_config = render_network_config("vlan_switch.j2",load_json_data_from_file("./data/vlan_ESW3.json"))
    return r03_config, esw3_config



if __name__ == "__main__":
    
    env = Environment(loader=FileSystemLoader("templates"))

    r02_config, esw2_config = create_vlan_config_cpe_marseille()
    save_built_config('config/vlan_R02.conf', r02_config)
    save_built_config('config/vlan_ESW2.conf', esw2_config)
    
    r03_config, esw3_config = create_vlan_config_cpe_paris()
    save_built_config('config/vlan_R03.conf', r03_config)
    save_built_config('config/vlan_ESW3.conf', esw3_config)
