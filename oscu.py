#!/usr/bin/env python
from __future__ import print_function
from sys import argv, stderr
from os import system
from time import sleep
import liblo


def print_e(*args, **kwargs):
    "Print on standard error, for things that should not be piped"
    # TODO use a logger, maybe
    print(*args, file=stderr, **kwargs)


def handle(port, cmd):
    "Do something on message"

    if hasattr(cmd, "__call__"):
        # when called from python
        callback = cmd
    else:
        # when called from bash
        def callback(path, msg):
            system("{} {} {}".format(cmd, path, " ".join(msg)))

    server = liblo.ServerThread(int(port))
    server.add_method(None, None, callback)  # wildcard callback
    server.start()

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        server.stop()


def print_log(port=1234):
    "Display every message received on the given port (default 1234)"

    print_e("Logging port:", port)
    print_e()

    def callback(path, msg):
        print(path, *msg)

    handle(port, callback)


def send(addr, path, *msg):
    "Send message on a given path: ip:port path msg"
    target = liblo.Address("osc.udp://" + addr + "/")
    liblo.send(target, path, *msg)


def forward(out_addr, in_port=1234):
    "Forward received messages: out_ip:out_port in_port"

    print_e("Forwarding  port:", in_port, "to", out_addr)
    print_e()

    def callback(path, msg):
        print(path, *msg)
        send(out_addr, path, *msg)

    handle(in_port, callback)


def main():
    "Main function, used when called as script"
    commands = {}

    def print_help():
        "Display commands description"
        print_e("Usage:")
        # generate help from docstrings
        for cmd in commands:
            print_e("  ", argv[0], cmd, "\t", commands[cmd].__doc__)

    commands["log"] = print_log
    commands["send"] = send
    commands["forward"] = forward
    commands["handle"] = handle
    commands["help"] = print_help

    if not argv[1:]:
        print_help()
        return

    cmd = argv[1]
    args = argv[2:]

    try:
        commands.get(cmd, print_help)(*args)
    except Exception as e:
        print_e(e)
        print_e()
        print_help()


if __name__ == "__main__":
    main()
