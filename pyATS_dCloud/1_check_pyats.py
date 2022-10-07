from pyats.topology import Testbed, Device
from genie.testbed import load
from multiprocessing.dummy import Pool as ThreadPool
import datetime
from datetime import datetime
import os
import argparse
from openpyxl import load_workbook


import logging
logging.basicConfig(filename='log_checks.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s : %(message)s')

cmds = ["show running-config",
        "show version"]
outputs_folder = ""
folder_type = ""
second_try=[]

def store_command(hostname, command, command_output):
    daytime = datetime.strftime(datetime.now(), "%d_%m_%y")
    try:
        log_name = command + '.txt'
        folder = os.path.join(outputs_folder, hostname)
        #folder = os.path.join(folder, daytime)

        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.debug('Creating the Folder:-> ' + str(folder))

        file_log = os.path.join(folder, log_name)
        #print (file_log)
        try:
            with open(file_log, 'w') as f:
                f.write(command_output)
            if os.path.exists(file_log):
                result = 'SUCCESS'
                logging.debug("Info - Log file: '{}' successfuly created:".format(file_log))

            else:
                result = 'FAIL'
                error_msg = "Error - Failed to create log file: " + file_log
                logging.deug(error_msg)
        except Exception as e:
            logging.debug("Error in file creation:\n{}".format(e))
    except Exception as e:
        logging.debug("Eror in file creation\n{}".format(e))
    return result


def Testbed_routine(hostname):

    uut = tb.devices[hostname]
    connected=False
    try:
        uut.connect(init_config_commands=[],connection_timeout=5,log_stdout=True)
        connected=True
    except:
        logging.debug("Error #1 in the connection to: '{}'".format(hostname))

    if connected:
        print('Device: "{}" connected, starting backups'.format(hostname))
        try:
            for cmd in cmds:
                output = uut.execute(cmd)
                store_command(hostname,cmd,output)
                logging.debug('Command: "{}" was stored for hostname: "{}"'.format(hostname,cmd))
        except Exception as e:
            logging.debug('Exception catched on Hostname: "{}" Cmd: "{}"\n{}'.format(hostname,cmd,e))
        print('Backups completed for device: "{}"'.format(hostname))


def pool_connection(maxthreads,hostname):
    start_time = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
    pool = ThreadPool(maxthreads)
    pool_result = []
    try:
        #pool.map (funcion to iterate)
        pool_result = pool.map(Testbed_routine,hostname)
    except UnboundLocalError:
        print("Error mapping threads to routine")

    pool.close()
    pool.join()

    end_time = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
    print("Info - Start Time:", start_time)
    print("Info - End Time:", end_time)
    print("")

    return pool_result

def Create_Testbed(user,pswd,hostnames,device_ips,jump_bool,jump_ip):
    testbed = Testbed('exampleTestbed')

    if jump_bool:
        jump_server = Device('jump_host',
                    connections = {
                        'mgmt': {
                            'protocol': 'ssh',
                            'ip': jump_ip,
                            'port': 10104
                        },
                    })
        jump_server.os = 'linux'
        jump_server.testbed = testbed
        jump_server.credentials['default'] = dict(username='cisco', password='pyats2022')

    for i in range(len(hostnames)):
        if jump_bool:
            dev = Device(hostnames[i],
                connections = {
                            'cli': {
                                'protocol': 'ssh',
                                'ip': device_ips[i],
                                'proxy': 'jump_host',
                                'login_creds': ['default', 'local']
                                },
                            })
        else:
            dev = Device(hostnames[i],
            connections = {
                        'cli': {
                            'protocol': 'ssh',
                            'ip': device_ips[i],
                            'login_creds': ['default']
                            },
                        })
        dev.os = 'iosxr'
        dev.testbed = testbed
        dev.credentials['default'] = dict(username=user, password=pswd)
        logging.debug('Device {} added to testbed'.format(hostnames[i]))
        del dev
    return testbed

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--file', help='Input File', required=True)
    parser.add_argument('--type', help='Type of checks', required=True, choices=['pre','post'])
    parser.add_argument('--credentials', help='Send vRouter creds in format user:pass', required=True)
    parser.add_argument('--jump', help='Send Jumphost IP', required=False)
    args=parser.parse_args()

    type_con = args.type
    file = args.file
    creds = args.credentials
    jump_bool = False
    jump_ip = ""
    if args.jump :
        jump_bool = True
        jump_ip = args.jump
    global outputs_folder
    if "pre" in type_con:
        os.system('rm -rf Precheck')
        outputs_folder = "Precheck"
        folder = "Precheck"
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.debug('Creating the Folder:-> ' + str(folder))

    if "post" in type_con:
        os.system('rm -rf Postcheck')
        outputs_folder = "Postcheck"
        folder = "Postcheck"
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.debug('Creating the Folder:-> ' + str(folder))

    user = creds.split(":")[0]
    password = creds.split(":")[1]

    full_table = load_workbook(file)
    commands = full_table['Commands']
    devices = full_table['Device Info']

    device_ips = []
    hostnames = []
    new_cmd = []

    for i in range(1, len(list(list(devices.columns)[0]))):
        hostnames.append(list(list(devices.columns)[0])[i].value)

    for i in range(1, len(list(list(devices.columns)[1]))):
        device_ips.append(list(list(devices.columns)[1])[i].value)

    for i in range(1, len(list(list(commands.columns)[0]))):
        new_cmd.append(list(list(commands.columns)[0])[i].value)

    for cmd in new_cmd:
        cmds.append(cmd)

    testbed = Create_Testbed(user,password,hostnames,device_ips,jump_bool,jump_ip)
    try:
        global tb
        tb = load(testbed)
    except Exception as e:
        logging.debug('Exception on load testbed:\n {}'.format(e))

    result = pool_connection(12,hostnames)
    if result:
        print("Success")

if __name__ == "__main__":
    main()

