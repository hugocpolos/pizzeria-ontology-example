#!/usr/bin/env python

"""
@file
@brief A simple client application for ordering pizzas from a pizzeria server.

This script connects to a pizzeria server, allows the user to place orders,
and handles communication with the server. It attempts to find an open
pizzeria, greets the server, and processes user input until the user decides
to exit by typing "bye".

@author Hugo Constantinopolos
"""

import socket


import time
import sys

HOST, PORT = "localhost", 9999


def get_open_pizzeria():
    """
    @brief Attempts to connect to a pizzeria server.

    Waits for 1 second before trying to establish a socket connection
    to the specified HOST and PORT. If the connection is refused,
    it prints an error message and exits the program.

    @return A socket object connected to the pizzeria.
    """
    time.sleep(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Could not find an open pizzeria.")
        sys.exit(1)
    return sock


def greet(sock):
    """
    @brief Sends a greeting message to the pizzeria server and prints the response.

    @param sock The socket object connected to the pizzeria server.
    """
    sock.sendall(bytes("new_customer", "utf-8"))
    received = str(sock.recv(1024), "utf-8")
    print(received)


def get_order_message_from_cli():
    """
    @brief Prompts the user for an order message.

    @return The order message input by the user.
    """
    return input("> ")


def order(sock):
    """
    @brief Handles the ordering process with the pizzeria.

    Continuously prompts the user for order messages until the user
    types "bye". Sends each order message to the server and prints
    the server's response.

    @param sock The socket object connected to the pizzeria server.
    """
    order_msg = str()
    while order_msg.lower() != "bye":
        order_msg = get_order_message_from_cli()
        if not order_msg:
            continue
        sock.sendall(bytes(order_msg, "utf-8"))
        received = str(sock.recv(1024), "utf-8")
        print(received)


def main():
    """
    @brief Main function that runs the client application.

    Looks for an open pizzeria, greets the server, and manages
    the ordering process. Closes the socket connection when done.
    """
    print("Looking for an open pizzeria...")
    pizzeria = get_open_pizzeria()
    greet(pizzeria)
    order(pizzeria)
    pizzeria.close()


if __name__ == "__main__":
    main()
