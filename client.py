#!/usr/bin/env python3

import socket
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

Player = {
	  'name'	: '',
	  'score'	: 0,
	  'leve'	: 0,
	  'lines'	: 0,
	  'fallingPiece': None,
	  'nextPiece'	: None,
	  'board'	: [],
	  'wins'	: 0,
	  'state'	: False
}

while Player['score'] < 10:
    msg = str(Player)
    print("Enviando dados: ", msg)
    msg = msg.encode()
    tcp.send(msg)
    r = tcp.recv(1024)
    r = r.decode()
    print ("Recebendo dados adversário: ", r)
    Player['score'] += 1

tcp.close()
