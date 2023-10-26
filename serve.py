import socket
from time import sleep
from threading import Thread

BUFFER_SIZE = 1024
TIME_OUT = 5

game_serv_addr = ('127.0.0.1',int(input('输入游戏服务器端口: ')))
p2p_serv_addr = (input('输入P2P服务器地址: '),9000)
udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def life_data():
    while True:
        udp.sendto('life'.encode(),p2p_serv_addr)
        sleep(10)

Thread(target=life_data).start()

udp.sendto('life'.encode(),p2p_serv_addr)


client_map = {}

def addr_to_ip(addr):
    return f'{addr[0]}:{str(addr[1])}'

def client_handler(sock,addr):
    try:
        while True:
            buf = sock.recv(BUFFER_SIZE)
            if not buf:
                break
            udp.sendto(buf,addr)
    except:
        pass
    finally:
        sock.close()
        client_map[addr_to_ip(addr)] = None

while True:
    try:
        buf,addr = udp.recvfrom(BUFFER_SIZE)
        ip = addr_to_ip(addr)
        if client_map.get(ip) == None:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(TIME_OUT)
            sock.connect(game_serv_addr)
            Thread(target=client_handler,args=[sock,addr]).start()
            client_map[ip] = sock

        client = client_map[ip]
        client.send(buf)
    except:
        pass
