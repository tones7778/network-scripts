#!/usr/bin/env python
# -*- coding: utf-8 -*-

from netmiko import *
from getpass import getpass
import pprint
import os
import socket

# Template file and TextFSM index
os.environ["NET_TEXTFSM"] = "/home/tones/code/network-python/ntc-templates/templates"

with open('switches_inventory.txt') as f:
    myswitch = f.readlines()
    #print(myswitch)

with open('cisco_show_commands.txt') as s:
    mycommands = s.readlines()
    #print(mycommands)

for item in myswitch[:]:
    ip = socket.gethostbyname(item.strip("\n"))
    print(ip)
    cisco_device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': "XXXXXX",
            'password': "XXXXXX",
            'port': 22,
            'secret': '',
            'verbose': False,
        }

    for item in mycommands[:]:
        print(item.strip("\n"))

        net_connect = ConnectHandler(**cisco_device)
        results = net_connect.send_command(item.strip("\n"), use_textfsm=True)
        #show_ip_int = net_connect.send_command('show ip int brief', use_textfsm=True)
        #show_version = net_connect.send_command('show version', use_textfsm=True)
        pprint.pprint(results)
        #pprint.pprint(show_version)
        #pprint.pprint(show_ip_int)

