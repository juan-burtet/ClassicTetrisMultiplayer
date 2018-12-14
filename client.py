#!/usr/bin/env python3

import socket
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print ('Para sair use CTRL+X\n')
msg = 'Hello!'

while msg != 'ok':
    msg = msg.encode()
    tcp.send (msg)
    print ('enviando: ', msg) 
    msg = 'ok'

r = ''
while r == "ack recebido":
    r = tcp.recv(1024)
    r = r.decode()
    print('r: ', r)
    
tcp.close()
