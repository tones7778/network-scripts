#!/usr/bin/env python
# -*- coding: utf-8 -*-

#catch bad password - test passed
#catch ssh login failed. - test passed
#read and write to file.
# add logging - test passed room for improvement
# add read and write to sqldb and or postgresql

from netmiko import *
from getpass import getpass
import pprint
import os
import logging

def main():
    logging.basicConfig(level=logging.INFO, filename='cisco_switch.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning('-----------------------Start logging-----------------------------')

    # Template file and TextFSM index
    os.environ["NET_TEXTFSM"] = "/home/tones/code/network-python/ntc-templates/templates"
    mypass = getpass()

    with open('cisco_switches_inventory.txt') as f:
        myswitch = f.readlines()
        logging.info('Reading inventory file ... %s: ', myswitch)

    with open('cisco_show_commands.txt') as s:
        mycommands = s.readlines()
        logging.info('Reading commands file ... %s: ', mycommands)


    for switch in myswitch[:]:
        try:
            device = switch.strip("\n")
            cisco_device = {'device_type': 'cisco_ios', 'host': device, 'username': 'tones', 'password': mypass, 'port': 22, 'secret': '', 'verbose': True,}
            print("Connecting to device: --> {}".format(device))
            net_connect = ConnectHandler(**cisco_device)
            logging.info('connected to %s: ', net_connect)

            try:
                for command in mycommands[:]:
                    print("Running command: --> {}".format(command.strip("\n")))
                    results = net_connect.send_command(command.strip("\n"))
                    pprint.pprint(results)

                    outputfile = open('cisco_switch_report.txt', 'a')
                    outputfile.write('*' * 80 + '\n')
                    outputfile.write('Command: ' + command + '\n')
                    outputfile.write('Device : ' + device + '\n')
                    outputfile.write(results + '\n')
                    outputfile.write('*' * 80 + '\n')

                    logging.debug('Running %s command: ', command)
            except Exception as e:
                print("ERROR!: {}".format(e))
                logging.error('%s raised an error', e)

        except Exception as e:
            print("ERROR!: {}".format(e))
            logging.error('%s raised an error', e)


    logging.warning('-----------------------Stop logging-------------------------------')

if __name__ == "__main__":
    main()
