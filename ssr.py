
#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import requests
import time
import os
import sys
import json
import socket

try:
    import netifaces
except ImportError:
    try:
        command_to_execute = "pip install netifaces || easy_install netifaces"
        print(command_to_execute)
    except OSError:
        print("Can NOT install netifaces, Aborted!")
        sys.exit(1)
    import netifaces

routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]

for interface in netifaces.interfaces():
    if interface == routingNicName:
        # print netifaces.ifaddresses(interface)
        routingNicMacAddr = netifaces.ifaddresses(
            interface)[netifaces.AF_LINK][0]['addr']
        try:
            routingIPAddr = netifaces.ifaddresses(
                interface)[netifaces.AF_INET][0]['addr']
            # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
            routingIPNetmask = netifaces.ifaddresses(
                interface)[netifaces.AF_INET][0]['netmask']
        except KeyError:
            pass

display_format = '%-30s %-20s'
print("Routing Gateway: "+routingGateway)
print("Routing NIC Name: "+routingNicName)
print("Routing NIC MAC Address: "+routingNicMacAddr)
print("Routing IP Address: "+routingIPAddr)
print("Routing IP Netmask: "+routingIPNetmask)

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(('8.8.8.8', 80))
# print(s.getsockname()[0])
# s.close()

response = requests.get("https://jsonip.com", proxies={
    'http': 'http://127.0.0.1:1080',
    'https': 'https://127.0.0.1:1080'
})
out_ip = json.loads(response.text)['ip']
print("外网IP: "+out_ip)
is_goon = input("确认上面信息无误，输入回车")
# print(sure_ip)
proxy_server_list=[]
proxy_ip_list=[]
def getHostName():
    with open('gui-config.json', 'r',encoding='utf-8') as f:
        for line in f.readlines():
            # print(line.strip())
            ser_ind=line.find('"server"')
            if ser_ind==-1:
                continue
            line=line[ser_ind+len('"server"'):].replace(":","").replace(",","").replace('''"''',"").strip()
            # print(line)
            proxy_server_list.append(line)
    return

def getIpList():
    for server in proxy_server_list:
        try:
            tmp=socket.gethostbyname(server)
            # print(tmp)
            proxy_ip_list.append(tmp)
        except:
            # print(server+" IP not get")
            continue

if len(is_goon) == 0:
    proxy_server_list = list(set(proxy_server_list))
    getHostName()
    getIpList()    
    temp_cmd = "route delete 0.0.0.0 mask 0.0.0.0"
    print(temp_cmd)
    temp_cmd = "route add 114.114.114.114 "+routingIPAddr+" metric 5"
    print(temp_cmd)
    temp_cmd = "route add 8.8.8.8 "+routingIPAddr+" metric 5"
    print(temp_cmd)
    for ip in proxy_ip_list:
        temp_cmd = "route add "+ip+" "+routingGateway+" metric 5"
        print(temp_cmd)
    temp_cmd = '''start cmd /k tun2socks.exe -proxyServer 127.0.0.1:1080 -tunAddr 10.0.0.2 -tunMask 255.255.255.0 -tunGw 10.0.0.1 -tunName "tun0901" -tunDns 8.8.8.8,114.114.114.114'''
    print(temp_cmd)
    temp_cmd = "route add 0.0.0.0 mask 0.0.0.0 10.0.0.1 metric 6"
    print(temp_cmd)
