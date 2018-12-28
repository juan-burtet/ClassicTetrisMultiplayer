#!/usr/bin/env python3

import socket
import _thread as thread

#HOST = '127.0.0.1'
HOST = '192.168.15.56'              # Endereco IP do Servidor
PORT = 5000                     # Porta que o Servidor esta

# Dict com status
Player1 = {
	  'name'	: '',
	  'score'	: 0,
	  'level'	: 0,
	  'lines'	: 0,
	  'fallingPiece': None,
	  'nextPiece'	: None,
	  'board'	: [],
	  'wins'	: 0,
	  'state'	: False
}

Player2 = {
	  'name'	: '',
	  'score'	: 0,
	  'level'	: 0,
	  'lines'	: 0,
	  'fallingPiece': None,
	  'nextPiece'	: None,
	  'board'	: [],
	  'wins'	: 0,
	  'state'	: False
}

mutex = thread.allocate_lock()

# Retorna um dict com os status

def conectado(con, cliente):
    global Player1
    global Player2
    
    print ('Conectado por', cliente)

    while True:
        # Recebe a mensagem
        clientMsg = con.recv(2048)
        if not clientMsg: break
        # Decodifica de byte para string
        clientMsg = clientMsg.decode()
        # Converte para dict
        clientDict = eval(clientMsg)

        # Pega os dados atuais dos players como string e codifica em byte
        mutex.acquire()
        player1Str = str(Player1)
        player2Str = str(Player2)
        mutex.release()
        player1Str = player1Str.encode()
        player2Str = player2Str.encode()
        
        # -----------------CASO DE INICIO DE PARTIDA-----------------
        # Se o nome do player 1 ainda não foi setado, atualiza
        mutex.acquire()
        if (Player1['name'] == ''):
            Player1 = clientDict
            print("Atualizando dados do Player1: ", clientMsg)
            # Responde com a string do player2
            con.send(player2Str)
            
        # Se o Player2 não foi setado e o cliente não é o player1, atualiza
        elif (Player2['name'] == '' and Player1['name'] != clientDict['name']):
            Player2 = clientDict
            print("Atualizando dados do Player2: ", clientMsg)
            # Responde com a string do player1
            con.send(player1Str)
            # Caso os dados recebidos sejam do player1
        elif (Player1['name'] == clientDict['name']):
            Player1 = clientDict
            print("Atualizando dados do Player1: ", clientMsg)
            # Responde com a string do player2
            con.send(player2Str)
        elif (Player2['name'] == clientDict['name']):
            Player2 = clientDict
            print("Atualizando dados do Player2: ", clientMsg)
            # Responde com a string do player1
            con.send(player1Str)
        mutex.release()
    
    print('Finalizando conexao do cliente', cliente)
    con.close()
    thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
