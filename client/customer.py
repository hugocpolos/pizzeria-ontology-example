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

import pickle
import socket
import sys
import time

import cowsay
import owlready2

HOST, PORT = "localhost", 9999
OWL_URL = "https://protege.stanford.edu/ontologies/pizza/pizza.owl"


def get_topping_name_of_pizza(pizza):
    return [x.prefLabel.first().title() for x in pizza.hasTopping]


def is_pizza_subclass_of(pizza, subclass_name):
    for super_class in pizza.ancestors():
        if super_class.name == subclass_name:
            return True
    return False


def is_vegetarian(pizza):
    return is_pizza_subclass_of(pizza, 'VegetarianPizza')


def is_spicy(pizza):
    return is_pizza_subclass_of(pizza, 'SpicyPizza')


def is_italian(pizza):
    return is_pizza_subclass_of(pizza, 'RealItalianPizza')


def get_pizza_description(pizza):
    vegetarian_text = "🌿 It is a vegetarian pizza 🌿"
    spicy_text = "🌶️  I should be cautious. This is a spicy pizza 🌶️"
    italian_pizza_text = "🤌  This is an authentic Italian pizza 🤌"

    toppings = get_topping_name_of_pizza(pizza)
    _is_vegetarian = is_vegetarian(pizza)
    _is_spicy = is_spicy(pizza)
    _is_italian = is_italian(pizza)

    return """
Look what a nice pizza that I've received!

It's a {} Pizza

{}

{}

{}

Ingredients:
{}""".format(pizza.name.title(), italian_pizza_text if _is_italian else '',
                   vegetarian_text if _is_vegetarian else '',
                   spicy_text if _is_spicy else '',
                   '\n'.join((f"  - {item}" for item in toppings)))


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


def customer_thoughts(message):
    return '\n'.join(cowsay.cowthink(message, cow='tux', width=40).split('\n')[0:-7])


def order(onto, sock):
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
        received = sock.recv(1024)
        try:
            received = str(received, "utf-8")
            print(received)
        except UnicodeDecodeError:
            received_pizza = onto.world._get_by_storid(pickle.loads(received))
            owlready2.sync_reasoner_hermit(infer_property_values=True, debug=False)
            print(customer_thoughts(get_pizza_description(received_pizza)))


def main():
    """
    @brief Main function that runs the client application.

    Looks for an open pizzeria, greets the server, and manages
    the ordering process. Closes the socket connection when done.
    """
    print("Looking for an open pizzeria...")
    onto = owlready2.get_ontology(OWL_URL).load()
    pizzeria = get_open_pizzeria()
    greet(pizzeria)
    order(onto, pizzeria)
    pizzeria.close()


if __name__ == "__main__":
    main()
