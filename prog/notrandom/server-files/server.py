#!/usr/bin/env python3

import os
import random
import socket
import secrets
import hashlib
from pathlib import Path
from argparse import ArgumentParser
from threading import Thread
from ruamel.yaml import safe_load


def get_commit(inst):
    jackpot = secrets.randbits(10)
    blind = inst.getrandbits(32)
    commit = hashlib.md5(str(jackpot+blind).encode()).hexdigest()
    return [commit,jackpot,blind]

class ClientThread(Thread):

    def __init__(self, ip, port, conn, flag):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.flag = flag
        self.conn.send("Hello and welcome to \"Will you get your degree\" challenge !  \n".encode())
        self.inst = random.Random()
        self.init_credit = 1000

    def run(self):
        while (self.init_credit>0):
            try:
                commit_result = get_commit(self.inst)
                self.conn.send(("To be sure we are fair, here is the commitment of our future jackpot %s\n"%(commit_result[0])).encode())
                self.conn.send("Pick your magic number between 0 and 2**10 : \n".encode())
                player_input = self.conn.recv(2048)
                try:
                    int_input = int(player_input)
                    if int_input == commit_result[1]:
                        self.init_credit+=100
                        self.conn.send("Good guess !\n".encode())
                    else:
                        self.init_credit-=500
                except ValueError:
                    self.conn.send('Please enter an integer\n'.encode())
                if(self.init_credit>10000):
                    self.conn.send((self.flag+"\n").encode())
                    break
                self.conn.send(("Commitment values : {0:04d} + {1:10d}\n".format(commit_result[1],commit_result[2])).encode())
                self.conn.send(("You have %d credits remaining\n"%(self.init_credit)).encode())
            except socket.error as e:
                print("Error",e)
                break
        self.conn.close()

if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('-c', '--config', type=Path, default=Path('.mkctf.yml'),
                   help="Configuration file.")
    args = p.parse_args()

    with open(args.config) as f:
        conf = safe_load(f)

    tcpHost = '0.0.0.0'
    tcpPort = conf['parameters']['port']
    flag = conf['flag']

    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((tcpHost, tcpPort))
    print("server listening on {}:{}".format(tcpHost, tcpPort))
    threads = []

    try:
        while True:
            tcpServer.listen()
            (conn, (ip, port)) = tcpServer.accept()
            print("new client from {}:{}".format(ip, port))
            newthread = ClientThread(ip, port, conn, flag)
            newthread.start()
            threads.append(newthread)

        for t in threads:
            t.join()
    except KeyboardInterrupt:
        os._exit(0)
