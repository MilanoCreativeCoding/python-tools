#!/usr/bin/env python
from __future__ import print_function
from sys import argv, stderr
from os import system
from time import sleep
import liblo

commands = {}


def print_e(*args, **kwargs):
    "Print on standard error, for things that should not be piped"
    # TODO use a logger, maybe
    print(*args, file=stderr, **kwargs)


def check_address(addr):
    "If only port is specified send to localhost"
    splitted = str(addr).split(":")
    if splitted[1:]:
        return addr
    else:
        return ":".join(["localhost", splitted[0]])


def handle(port, action):
    """port action
    Do something on message"""

    if hasattr(action, "__call__"):
        # when called from python
        callback = action
    else:
        # when called from bash
        def callback(path, msg):
            system("{} {} {}".format(action, path, " ".join(msg)))

    server = liblo.ServerThread(int(port))
    server.add_method(None, None, callback)  # wildcard callback
    server.start()

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        server.stop()


def print_log(port):
    """port
    Display every message received on the given port"""

    print_e("Logging port:", port)
    print_e()

    def callback(path, msg):
        print(path, *msg)

    handle(port, callback)


def send(addr, path, *msg):
    """address path message
    Send message on a given path"""
    addr = check_address(addr)
    target = liblo.Address("osc.udp://" + addr + "/")
    liblo.send(target, path, *msg)


def forward(port, addr):
    """port address
    Forward received messages to address"""
    addr = check_address(addr)

    print_e("Forwarding  port:", port, "to", addr)
    print_e()

    def callback(path, msg):
        print(path, *msg)
        send(addr, path, *msg)

    handle(port, callback)


def print_help(cmd=None):
    """[command]
    Display commands description"""
    if cmd:
        # generate help from docstrings
        print_e(argv[0], cmd,  commands[cmd].__doc__)
    else:
        # list commads
        print_e("Commands:")
        for cmd in commands:
            print_e("    ", cmd)
        print_e("for details call:", argv[0], "help command")


def main():
    "Main function, used when called as script"

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
        print_help(cmd)


if __name__ == "__main__":
    main()
