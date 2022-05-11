from netmiko import ConnectHandler
import json

def question_25(net_connect):
    command = "show ip int brief"
    output = net_connect.send_command(command)
    print(output)


def question_26(net_connect):
    command = "show ip int brief"
    output = net_connect.send_command(command,use_textfsm=True)
    print(output)



def question_27(net_connect):
    command = "show ip route"
    output = net_connect.send_command(command,use_textfsm=True)
    print(output)


def question_28(net_connect):
    command = "show ip int brief"
    output = net_connect.send_command(command,use_textfsm=True)
    
    for interface in output:
        print(interface["intf"], " : ", interface["status"])

    for interface in output:
        command = "show run int " + interface["intf"]
        output = net_connect.send_command(command,use_textfsm=True)
        print(output)

def question_29(net_connect):
    command = ["int loopback 1"]
    command += ["ip address 192.168.1.1 255.255.255.255"]
    command += ["description loopback interface from netmiko"]
    command += ["no sh"]
    output = net_connect.send_config_set(config_commands = command)
    output += net_connect.save_config()
    print(output)


def question_30(net_connect):
    command = ["no int loopback 1"]    
    output = net_connect.send_config_set(config_commands = command)
    output += net_connect.save_config()
    print(output)


def question_31(net_connect):
    output = net_connect.send_config_from_file("./config/loopback_R01.conf")
    output += net_connect.save_config()
    print(output)


def question_32(net_connect):
    command = ["no int loopback 1"] 
    command += ["no int loopback 2"]   
    command += ["no int loopback 3"]   
    command += ["no int loopback 4"]      
    output = net_connect.send_config_set(config_commands = command)
    output += net_connect.save_config()
    print(output)


def get_inventory():

    file_path = "./inventory/hosts.json"

    try:
        with open(file_path) as f:
            data = json.load(f)
            f.close()
    
    except IOError:
        print("Could not read file:", file_path)

    return data



def question_35():
    hosts = get_inventory()
    for host in hosts:
        if "R" in host["hostname"]:
            tmp = host.pop("hostname", None)
            net_connect = ConnectHandler(**host)
            command = "show run int g0/0.99"
            output = net_connect.send_command(command,use_textfsm=True)
            print(tmp ," :", output)


def question_36():
    hosts = get_inventory()
    for host in hosts:
        if host["hostname"] == "R02" or host["hostname"] == "R03" or host["hostname"] == "ESW2" or host["hostname"] == "ESW3":
            tmp = host.pop("hostname", None)
            net_connect = ConnectHandler(**host)
            file_config = "./config/vlan_" + tmp + ".conf"
            output = net_connect.send_config_from_file(file_config)
            output += net_connect.save_config()
            print(tmp," : ",output)
        
      

if __name__ == "__main__":    
    
    r01 = {
        'device_type': 'cisco_ios',
        'host': '172.16.100.126',
        'username': 'cisco',
        'password': 'cisco'
    }

    net_connect = ConnectHandler(**r01)
    #print(net_connect.__dict__)
    #question_25(net_connect)
    #question_26(net_connect)
    #question_27(net_connect)
    #question_28(net_connect)
    #question_29(net_connect)
    #question_30(net_connect)
    #question_31(net_connect)
    #question_32(net_connect)
    #question_35()
    question_36()

