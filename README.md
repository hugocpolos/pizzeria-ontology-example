# Pizza Ontology Client-Server Application

## Overview

This project implements a client-server application that uses the Pizza Ontology to illustrate the
principles of ontology-oriented programming (OOP). The application simulates a pizzeria where
clients can place orders and interact with the ontology to understand how semantic technologies
enhance software development.

## Features

- **Client-Server Architecture**: Customers can see the menu and order pizzas from a server
  (pizzeria).
- **Pizza Ontology Integration**: Utilizes the Pizza Ontology for structured representation of pizza
  types and ingredients.
- **Interactive Command-Line Interface**: Clients can input orders, and the server responds based on
  the ontology.
- **Textual Representation of a pizza**: Customers, knowing the ontology, describes what they have
  received from the pizzeria.
## Prerequisites

- Python 3.x
- `owlready2` library
- `python-cowsay` library (yes...)

## Usage

### Starting the Server

Run the server script to listen for incoming connections:
```bash
python server/pizza_place.py
```

### Running the Client

In a separate terminal, run the client script to connect to the server and place orders:
```bash
python client/customer.py
```

Follow the on-screen prompts to interact with the pizzeria.

