import owlready2


class PizzaOntologyHandler:
    OWL_URL = "https://protege.stanford.edu/ontologies/pizza/pizza.owl"

    def __init__(self):
        self.onto = owlready2.get_ontology(self.OWL_URL).load()
        owlready2.sync_reasoner_hermit(infer_property_values=True, debug=False)

    def get_all_named_pizzas(self):
        _named_pizzas = [i for i in self.onto.classes() if i.name == 'NamedPizza'][0]
        return [i for i in _named_pizzas.descendants() if i.name != 'NamedPizza']

    def get_name_of_all_named_pizzas(self):
        return [i.name for i in self.get_all_named_pizzas()]

    def get_pizza_by_name(self, pizza_name):
        pizzas = [i for i in self.get_all_named_pizzas() if i.name.lower() == pizza_name.lower()]

        if len(pizzas) == 0:
            return None

        return pizzas[0]

    def get_topping_name_of_pizza(self, pizza):
        return [x.prefLabel.first().title() for x in pizza.hasTopping]

    def is_pizza_subclass_of(self, pizza, subclass_name):
        for super_class in pizza.ancestors():
            if super_class.name == subclass_name:
                return True
        return False

    def is_vegetarian(self, pizza):
        return self.is_pizza_subclass_of(pizza, 'VegetarianPizza')

    def is_spicy(self, pizza):
        return self.is_pizza_subclass_of(pizza, 'SpicyPizza')

    def is_italian(self, pizza):
        return self.is_pizza_subclass_of(pizza, 'RealItalianPizza')


onto = owlready2.get_ontology(PizzaOntologyHandler.OWL_URL).load()
