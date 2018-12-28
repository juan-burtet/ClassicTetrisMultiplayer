import socket

#HOST = '127.0.0.1'              # Endereco IP do Servidor
HOST = '192.168.15.56'   
PORT = 5000                     # Porta que o Servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

#while True:
#    con, cliente = tcp.accept()
#    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
