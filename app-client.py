#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libclient

sel = selectors.DefaultSelector()


def create_request(action, player):
    if action == "hello" || "update" :
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, player=player), # mudar value para um dict com tudo do PLAYE
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + value, encoding="utf-8"),
        )


def start_connection(host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)


if len(sys.argv) != 5:
    print("usage:", sys.argv[0], "<host> <port> <action> <value>")
    sys.exit(1)

player1 = {
    "id"        : 0,
    "name"      : "",
    "score"     : "",
    "level"     : "",
    "lines"     : 0,
    "nextBlock" : "",
    "board"     : "",
    "wins"      : 0,
    "state"     : "",
}

player2 = {
    "id"        : 0,
    "name"      : "",
    "score"     : "",
    "level"     : "",
    "lines"     : 0,
    "nextBlock" : "",
    "board"     : "",
    "wins"      : 0,
    "state"     : "",
}



host, port = sys.argv[1], int(sys.argv[2])
action = "hello"
request = create_request(action, player1)
start_connection(host, port, request)
r1 = None

try:
    events = sel.select(timeout=1)
    for key, mask in events:
        message = key.data
        try:
           message.process_events(mask)
           r1 = message.response
        except Exception as e:
           print(
                "main: error: exception for",
                f"{message.addr}:\n{traceback.format_exc()}",
            )
            message.close()
    # Check for a socket being monitored to continue.
    if not sel.get_map():
        break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")

player1["ID"] = response["ID"]
action = "update"
request = create_request(action, player1)


try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
            except Exception as e:
                print(
                    "main: error: exception for",
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
                message.close()
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
