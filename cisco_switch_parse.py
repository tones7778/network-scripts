#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://pynet.twb-tech.com/blog/automation/netmiko-textfsm.html
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

for item in myswitch[:]:
    ip = socket.gethostbyname(item.strip("\n"))
    print(ip)
    cisco_device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': "XXXXX",
            'password': "XXXXX",
            'port': 22,
            'secret': '',
            'verbose': False,
        }

    net_connect = ConnectHandler(**cisco_device)

    show_ip_int = net_connect.send_command('show ip int brief', use_textfsm=True)
    show_version = net_connect.send_command('show version', use_textfsm=True)

    pprint.pprint(show_version)
    pprint.pprint(show_ip_int)

