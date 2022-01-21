#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import time

PORT = 9090

def destroy_sockets(server: socket.socket, client: socket.socket):
    server.close()
    client.close()

def threadConnectClient(client: socket.socket, addr):
    try:
        server = socket.socket()
        data = client.recv(16384)
        if data[0] != 5:
            response = b'\x05\xFF'
            client.sendall(response)
            destroy_sockets(server, client)
            return 0
        for i in range(0, int(data[1])):
            if data[2+i] == 0:
                response = b'\x05\x00'
                client.sendall(response)
                # bind_addr = bytes([192, 168, 0, 145]) + bytes([90, 90])
                break
            elif data[2+i] == 1:
                response = b'\x05\x01'
                client.sendall(response)
                data = client.recv(16384)
                print(f'{data}')
                response = b'{data[0]}\xFF'
                client.sendall(response)
                destroy_sockets(server, client)
                return 0
            elif data[2+i] == 2:
                response = b'\x05\x02'
                client.sendall(response)
                data = client.recv(16384)
                response = b'\x01\x00'
                client.sendall(response)
                # bind_addr = bytes([192, 168, 0, 145]) + bytes([90, 90])
                break
            elif i == int(data[1]):
                response = b'\x05\xFF'
                client.sendall(response)
                destroy_sockets(server, client)
                return 0
        data = client.recv(16384)

        if data[3] == 1:
            dst_addr = socket.inet_ntoa(data[4:8])
            dst_port = int.from_bytes(data[8:10], byteorder="big")
        elif data[3] == 3:
            fqdn_len = data[4]
            print(f'CONN: Resolving {data[5:5+fqdn_len]}')
            dst_port = int.from_bytes(data[5+fqdn_len:5+fqdn_len+3], byteorder="big")
            try:
                addr_info = socket.getaddrinfo(data[5:5+fqdn_len].decode("utf8"), dst_port, family=socket.AF_INET)
                dst_addr = addr_info[0][4][0]
            except:
                dst_addr = data[5:5+fqdn_len]
        else:
            print(f"{data[3]}")
        print(f'CONN: Connecting to {dst_addr}:{dst_port}')
        server.connect((dst_addr, dst_port))
        print(f"CONN: Connected to {dst_addr}:{dst_port}")
        response = b'\x05\x00\x00\x01\x00\x00\x00\x00' + bytes([int(PORT / 100), PORT % 100])
        client.sendall(response)

        threading.Thread(
            target=threadFromClientToServer,
            args=(client, server)
            ).start()
        threading.Thread(
            target=threadFromServerToClient,
            args=(client, server)
            ).start()
    except Exception as e:
        print(repr(e))
        destroy_sockets(server, client)


def threadFromClientToServer(client, server):
    try:
        while True:
            data = client.recv(16384)
            if len(data) == 0:
                break
            server.sendall(data)
    except Exception as e:
        print(repr(e))
        return


def threadFromServerToClient(client, server):
    try:
        while True:
            data = server.recv(16384)
            if len(data) == 0:
                break
            client.sendall(data)
    except Exception as e:
        print(repr(e))
        return


sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 9090))

print('Listening on 9090')
while True:
    try:
        sock.listen()

        try:
            client, addr = sock.accept()
            threading.Thread(
                target=threadConnectClient,
                args=(client, addr)
                ).start()
            # time.sleep(10)
        except Exception as f:
            print(repr(f))
    except Exception as e:
        print(repr(e))
        print("Closing socket")
        sock.close()
        time.sleep(1)
