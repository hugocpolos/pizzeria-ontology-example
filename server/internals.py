import re
import socketserver
import time

import pizza_ontology_handler


class _CustomerConnectionHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        self.data = None
        super().__init__(*args, **kwargs)

    def handle(self):
        self.data = self.request.recv(1024).strip()
        if self.data == b'new_customer':
            self.pizza_knowledge = pizza_ontology_handler.PizzaOntologyHandler()
            self.handle_customer_service()

    def server_log(self, message):
        print(f"[{self.client_address[0]}:{self.client_address[1]}] {message}")

    def handle_customer_service(self):
        self.server_log("New customer")
        self.request.sendall("Welcome to Pizza Place, how can i help you?".encode())
        self.service_main_loop()
        self.server_log("Customer left")

    def service_main_loop(self):
        while self.data.decode().lower() != "bye":
            self.data = self.request.recv(1024).strip()
            self.server_log(f"Received: {self.data.decode()}")
            self.parse(self.data.decode())

    def parse(self, order):
        if order.lower() == 'bye':
            return None

        if self.is_greeting(order):
            return self.greet_back()

        if self.wants_menu(order):
            return self.send_menu()

        if self.wants_pizza(order):
            return self.process_order(order)

        return self.did_not_understand()

    def is_greeting(self, msg):
        msg = msg.lower().strip()
        return msg in ['hello', 'hi', 'hey', 'good morning', 'good evening', 'good afternoon']

    def wants_menu(self, msg):
        msg = msg.lower()
        return "menu" in msg

    def wants_pizza(self, msg):
        msg = msg.lower()
        return msg.startswith("i want")

    def did_not_understand(self):
        self.request.sendall("Sorry, I couldn't understand".encode())

    def we_dont_have_this(self, resource_name):
        self.request.sendall(
            f"Sorry, we don't have {resource_name} at Pizza Place".encode())

    def greet_back(self):
        self.request.sendall(
            """
Hello, welcome to Pizza Place :)

You can either ask for the menu or order a pizza using the pizza place chat bot.
""".encode())

    def send_menu(self):
        menu = self.pizza_knowledge.get_name_of_all_named_pizzas()
        menu_content = '\n'.join((f"  - {item}" for item in menu))
        self.request.sendall(
            f"""
Of course, here is the menu:

{menu_content}
        """.encode())

    def process_order(self, order):
        order = order.lower()
        order_re = r'i want.*\s(\w+)$'
        match_order = re.search(order_re, order, re.IGNORECASE)

        if match_order is None:
            return self.did_not_understand()

        pizza_name = match_order.group(1)

        pizza = self.pizza_knowledge.get_pizza_by_name(pizza_name)

        if pizza is None:
            return self.we_dont_have_this(pizza_name)

        return self.request.sendall(f"{self.get_pizza_description(pizza)}".encode())

    def get_pizza_description(self, pizza):

        vegetarian_text = "🌿 It is a vegetarian pizza 🌿\n"
        spicy_text = "🌶️  Be cautious. This is a spicy pizza 🌶️\n"
        italian_pizza_text = "🤌  This is an authentic Italian pizza 🤌\n"

        toppings = self.pizza_knowledge.get_topping_name_of_pizza(pizza)
        is_vegetarian = self.pizza_knowledge.is_vegetarian(pizza)
        is_spicy = self.pizza_knowledge.is_spicy(pizza)
        is_italian = self.pizza_knowledge.is_italian(pizza)
        return """
Here it is your '{}' pizza!

{}{}{}
Ingredients:
{}
        """.format(pizza.name.title(), italian_pizza_text if is_italian else '',
                   vegetarian_text if is_vegetarian else '',
                   spicy_text if is_spicy else '',
                   '\n'.join((f"  - {item}" for item in toppings)))


class _PizzaPlaceServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def get_pizza_place_multithreaded_tcp_server(host, port):
    timeout_size = 60  # attempts
    while timeout_size > 0:
        try:
            return _PizzaPlaceServer((host, port), _CustomerConnectionHandler)
        except OSError:
            timeout_size -= 1
            time.sleep(1)
    return None
