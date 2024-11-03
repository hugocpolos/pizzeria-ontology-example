#!/usr/bin/env python

import sys

import internals

HOST, PORT = "localhost", 9999


def main():
    print("Opening Pizza Place ...")
    pizza_place = internals.get_pizza_place_multithreaded_tcp_server(HOST, PORT)

    if pizza_place is None:
        print("Could not open pizza place. Exiting")
        return 1

    print("Pizza Place is open and waiting for customers")
    pizza_place.serve_forever()
    pizza_place.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
