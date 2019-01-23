#!/usr/bin/env python
# -*- coding: utf-8 -*-

from netmiko import *
from getpass import getpass
import pprint

def cisco_sw03(username, password):
    cisco_device = {
        'device_type': 'cisco_ios',
        'ip':   '192.168.2.57',
        'username': username,
        'password': password,
        'port': 22,          # optional, defaults to 22
        'secret': '',     # optional, defaults to ''
        'verbose': False,       # optional, defaults to False
    }

    net_connect = ConnectHandler(**cisco_device)

    output = net_connect.send_command('show ip int brief', use_textfsm=True)

    pprint.pprint(output)

if __name__ == "__main__":
    cisco_sw03('tones', getpass())
