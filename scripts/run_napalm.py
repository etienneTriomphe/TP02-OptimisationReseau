from napalm import get_network_driver
from jinja2 import Template, Environment, FileSystemLoader
import json

def get_inventory():
    file_path = "./inventory/hosts.json"

    try:
        with open(file_path) as f:
            data = json.load(f)
            f.close()
    
    except IOError:
        print("Could not read file:", file_path)

    return data

def save_built_config(file_name, data):
    try:
        with open(file_name, "w") as f:
            f.write(data)
            f.close()
    
    except IOError:
        print("Could not read file:", file_name)

def render_network_config(template_name, data):
    template = env.get_template(template_name) 
    return template.render(data) 

def load_json_data_from_file(file_path):
    try:
        with open(file_path) as f:
            data = json.load(f)
            f.close()
    
    except IOError:
        print("Could not read file:", file_path)

    return data


def question_41(device):
    command = ["show ip int brief"]
    print(device.cli(command))


def question_43(device):
    print(device.get_arp_table())


def question_45(device):
        
    device.load_merge_candidate("config/loopback_R01_napalm.conf")
    print(device.compare_config())
    device.commit_config()
    
    

def question_46():

    ospf_r01_config = render_network_config("ospf.j2",load_json_data_from_file("data/ospf_r01.json"))
    ospf_r02_config = render_network_config("ospf.j2",load_json_data_from_file("data/ospf_r02.json"))
    ospf_r03_config = render_network_config("ospf.j2",load_json_data_from_file("data/ospf_r03.json"))

    save_built_config('config/ospf_r01.conf', ospf_r01_config)
    save_built_config('config/ospf_r02.conf', ospf_r02_config)
    save_built_config('config/ospf_r03.conf', ospf_r03_config)
    

def question_47(device_r01,device_r02,device_r03):
    device_r01.load_merge_candidate("config/ospf_r01.conf")
    device_r01.commit_config()
    device_r02.load_merge_candidate("config/ospf_r02.conf")
    device_r02.commit_config()
    device_r03.load_merge_candidate("config/ospf_r03.conf")
    device_r03.commit_config()
    

def question_49(driver):
    hosts = get_inventory()
    for host in hosts:
        device_host = {
        'hostname': host["ip"],
        'username': host["username"],
        'password': host["password"]
        }

        device = driver(**device_host)
        device.open()
        response = device.get_config()
        filepath = "config/backup/"+host["hostname"]+".bak"
        save_built_config(filepath, response["running"])

if __name__ == "__main__":

    env = Environment(loader=FileSystemLoader("templates"))

    r01 = {
    'hostname':'172.16.100.126',
    'username': 'cisco',
    'password': 'cisco'
    }
    r02 = {
    'hostname':'172.16.100.190',
    'username': 'cisco',
    'password': 'cisco'
    }
    r03 = {
    'hostname':'172.16.100.254',
    'username': 'cisco',
    'password': 'cisco'
    }
    driver = get_network_driver('ios')
    device_r01 = driver(**r01)
    device_r01.open()
    device_r02 = driver(**r02)
    device_r02.open()
    device_r03 = driver(**r03)
    device_r03.open()
    #question_41(device)
    #question_43(device)
    #question_45(device)
    #question_46()
    #question_47(device_r01,device_r02,device_r03)
    question_49(driver)
    