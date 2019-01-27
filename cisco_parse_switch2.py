#!/usr/bin/env python
# -*- coding: utf-8 -*-

from netmiko import *
from getpass import getpass
import pprint
import os
import logging
import json

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
            with open('cisco_switch_report.json', 'a') as json_out_file:
                json_out_file.write('\n\n' + 'Device : ' + device + '\n')

            logging.info('connected to %s: ', net_connect)

            try:
                for command in mycommands[:]:
                    print("Running command: --> {}".format(command.strip("\n")))

                    # save results as json
                    results_json = net_connect.send_command(command.strip("\n"), use_textfsm=True)
                    pprint.pprint(results_json)
                    with open('cisco_switch_report.json', 'a') as command_out:
                        command_out.write('Command: ' + command + '\n')
                        json.dump(results_json, command_out, sort_keys=True, indent=4)

                    # save results as a report
                    # results = net_connect.send_command(command.strip("\n"))
                    # pprint.pprint(results)
                    # outputfile = open('cisco_switch_report.txt', 'a')
                    # outputfile.write('*' * 80 + '\n')
                    # outputfile.write('Command: ' + command + '\n')
                    # outputfile.write('Device : ' + device + '\n')
                    # outputfile.write(results + '\n')
                    # outputfile.write('*' * 80 + '\n')

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
