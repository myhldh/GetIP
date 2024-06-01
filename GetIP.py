import binascii
import random
from socket import *
def get_ip(local_port:int=8888,stun_server:str='stun.l.google.com',stun_port:int=19302,csock:socket=None):
    tranid=''.join(random.choice('0123456789ABCDEF') for i in range(32))
    data=binascii.a2b_hex('00010000'+tranid)
    sock=None
    if csock==None:
        sock=socket(AF_INET,SOCK_DGRAM)
        sock.bind(('0.0.0.0',local_port))
    else:
        sock=csock
    sock.sendto(data,(stun_server,stun_port))
    buf,addr=sock.recvfrom(2048)
    if csock==None:
        sock.close()
    if tranid.upper()==binascii.b2a_hex(buf[4:20]).upper().decode() and binascii.b2a_hex(buf[0:2]).decode()=='0101':
        port = int(binascii.b2a_hex(buf[26:28]), 16)
        ip = ".".join([
            str(int(binascii.b2a_hex(buf[28:29]), 16)),
            str(int(binascii.b2a_hex(buf[29:30]), 16)),
            str(int(binascii.b2a_hex(buf[30:31]), 16)),
            str(int(binascii.b2a_hex(buf[31:32]), 16))
        ])
        return (ip+':'+str(port))
    return 'Failed'
def ip_tuple(local_port:int=8888,stun_server:str='stun.l.google.com',stun_port:int=19302,csock:socket=None):
    ret=get_ip(local_port,stun_server,stun_port,csock)
    if ret=='Failed':
        return 'Failed'
    ret=ret.split(':')
    return (ret[0],int(ret[1]))
if __name__=='__main__':
    print(get_ip())