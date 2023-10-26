import socket
from threading import Thread

BUFFER_SIZE = 1024
TIME_OUT = 5

p2p_serv_addr = (input('输入P2P服务器地址: '),9000)
def get_server_port(ip):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(f'ip {ip}'.encode(),p2p_serv_addr)
    buf,_ = sock.recvfrom(BUFFER_SIZE)
    sock.close()
    return int(buf.decode())

server_ip = input('输入服务器地址: ')
server_addr = (server_ip,get_server_port(server_ip))

tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp.bind(('0.0.0.0',9001))
tcp.listen()

def get_server_data(tcp_sock,udp_sock):
    try:
        while True:
            buf,_ = udp_sock.recvfrom(BUFFER_SIZE)
            tcp_sock.send(buf)
    except:
        pass

def client_handler(sock):
    udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_sock.sendto(b'hello',p2p_serv_addr)
    Thread(target=get_server_data,args=[sock,udp_sock]).start()
    try:
        while True:
            buf = sock.recv(BUFFER_SIZE)
            if not buf:
                break
            udp_sock.sendto(buf,server_addr)
    except:
        pass
    finally:
        sock.close()
        udp_sock.close()

while True:
    sock,_ = tcp.accept()
    sock.settimeout(TIME_OUT)
    Thread(target=client_handler,args=[sock]).start()
