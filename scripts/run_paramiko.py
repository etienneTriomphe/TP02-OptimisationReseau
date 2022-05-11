import time
import paramiko

def question_11(remote_conn, nbytes):
    remote_conn.send("show ip interface brief \n") 
    time.sleep(.5)
    output = remote_conn.recv(nbytes) #Get output data from the channel
    print(output.decode("UTF-8"))


def question_15(remote_conn, nbytes):
    commande = "conf t \n"
    commande += "int lo1 \n"
    commande += "ip address 192.168.1.1 255.255.255.255 \n"
    commande += "description loopback interface from paramiko \n"
    commande += "no shut \n" 
    commande += "end \n"
    remote_conn.send(commande) 
    time.sleep(.5)
    output = remote_conn.recv(nbytes) #Get output data from the channel
    print(output.decode("UTF-8"))

def question_16(remote_conn, nbytes):
    commande = "sh run int lo1\n"
    remote_conn.send(commande) 
    time.sleep(.5)
    output = remote_conn.recv(nbytes) #Get output data from the channel
    print(output.decode("UTF-8"))


def question_17(devices, nbytes):

    commande = "sh int summary\n"
    for device in devices:
        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device.get('ip'),
            username=device.get('username'),
            password=device.get('password'),
            look_for_keys=False, allow_agent=False,
            timeout=5)
        remote_conn = ssh.invoke_shell()
        remote_conn.send(commande) 
        time.sleep(1)
        output = remote_conn.recv(nbytes) #Get output data from the channel
        print(output.decode("UTF-8"))
        ssh.close()



def question_18(devices, nbytes):
    commande = "conf t\n"
    commande += "int g0/0.99\n"
    commande += "description sub-interface for admin vlan access - set by paramiko\n"
    commande += "end\n"
    commande += "sh run int g0/0.99\n"
    for device in devices:
        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device.get('ip'),
            username=device.get('username'),
            password=device.get('password'),
            look_for_keys=False, allow_agent=False,
            timeout=5)
        remote_conn = ssh.invoke_shell()
        remote_conn.send(commande) 
        time.sleep(1)
        output = remote_conn.recv(nbytes) #Get output data from the channel
        print(output.decode("UTF-8"))
        ssh.close()

def save_config(devices, nbytes):
    commande = "sh run\n"
    for device in devices:
        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device.get('ip'),
            username=device.get('username'),
            password=device.get('password'),
            look_for_keys=False, allow_agent=False,
            timeout=5)
        remote_conn = ssh.invoke_shell()
        remote_conn.send(commande) 
        time.sleep(1)
        output = remote_conn.recv(nbytes) #Get output data from the channel
        print(output.decode("UTF-8"))
        ssh.close()

        file_name = "config/backup/backup_" + device.get('hostname') + ".conf"

        try:
            with open(file_name, "w") as f:
                f.write(output.decode("UTF-8"))
                f.close()
    
        except IOError:
            print("Could not read file:", file_name)



if __name__ == "__main__":

    device = {
        "hostname": "R1",
        "ip": "172.16.100.126",
        "username": "cisco",
        "password": "cisco"
    }

    device2 = {
        "hostname": "R2",
        "ip": "172.16.100.190",
        "username": "cisco",
        "password": "cisco"
    }

    device3 = {
        "hostname": "R3",
        "ip": "172.16.100.254",
        "username": "cisco",
        "password": "cisco"
    }
    ssh = paramiko.SSHClient() #initialization of SSHClient class
    #Set policy to use when connecting to servers without a known host key
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #init connection with the remote device
    ssh.connect(device.get('ip'),
            username=device.get('username'),
            password=device.get('password'),
            look_for_keys=False, allow_agent=False,
            timeout=5)

    nbytes = 65535
    #get the remote shell
    remote_conn = ssh.invoke_shell()
    
    #question_11(remote_conn, nbytes)

    #question_15(remote_conn, nbytes)

    #question_16(remote_conn, nbytes)

    ssh.close()

    #question_17([device2,device3], nbytes)

    #question_18([device,device2,device3], nbytes)

    save_config([device,device2,device3], nbytes)

   