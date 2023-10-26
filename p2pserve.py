import socket
from threading import Thread
from time import time,sleep

BUFFER_SIZE = 1024
udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp.bind(('0.0.0.0',9000))

ip_map = {}

def clean_ip_map():
    while True:
        keys = ip_map.keys()
        for v in keys:
            if ip_map.get(v) == None:
                continue
            if (time() - ip_map[v]['time']) > 120:
                ip_map[v] = None
        sleep(5)

Thread(target=clean_ip_map).start()

def cache_address(addr):
    ip_map[addr[0]] = {'port':addr[1],'time':int(time())}

def get_address(data,addr):
    if ip_map.get(data) == None:
        return
    udp.sendto(str(ip_map[data]['port']).encode(),addr)

while True:
    buf,addr = udp.recvfrom(BUFFER_SIZE)
    try:
        data = buf.decode()
        if data[:4] == 'life':
            cache_address(addr)
        elif data[:2] == 'ip':
            get_address(data[3:],addr)
    except:
        pass