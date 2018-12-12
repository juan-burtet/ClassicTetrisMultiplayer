#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libserver

sel = selectors.DefaultSelector()
host = "127.0.0.1"
port = 65432


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)

host = "127.0.0.1"
port = 65432

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


player1 = {
    "id"        : 0,
    "name"      : "",
    "score"     : 0,
    "level"     : 0,
    "lines"     : 0,
    "nextBlock" : "",
    "board"     : "",
    "wins"      : 0,
    "state"     : ""
}

player2 = {
    "id"        : 0,
    "name"      : "",
    "score"     : 0,
    "level"     : 0,
    "lines"     : 0,
    "nextBlock" : "",
    "board"     : "",
    "wins"      : 0,
    "state"     : ""
}



try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.setPlayer1(player1)
                    message.setPlayer2(player2)
                    message.process_events(mask)
                    player1 = message.getPlayer1()
                    player2 = message.getPlayer2()

                except Exception:
                    print(
                        "main: error: exception for",
                        )
                    message.close()

except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
