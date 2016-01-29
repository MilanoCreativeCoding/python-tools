#!/usr/bin/env python
from __future__ import print_function
from sys import argv
from time import sleep
import liblo


def print_log(port=7172):
    "Display every message received on the given port (optional)"
    port = int(port)

    print("Logging port:", port)
    print()

    def callback(path, args):
        print(path, *args)

    server = liblo.ServerThread(port)
    server.add_method(None, None, callback)  # wildcard callback
    server.start()

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        server.stop()


# TODO: send, foward, etc...


def main():
    "Main function, used when called as script"
    commands = {}

    def print_help():
        "Display commands description"
        print("Usage:")
        # generate help from docstrings
        for cmd in commands:
            print("  ", argv[0], cmd, "\t", commands[cmd].__doc__)

    commands["log"] = print_log
    commands["help"] = print_help

    if not argv[1:]:
        print_help()
        return

    cmd = argv[1]
    args = argv[2:]

    try:
        commands.get(cmd, print_help)(*args)
    except Exception as e:
        print(e)
        print()
        print_help()


if __name__ == "__main__":
    main()
