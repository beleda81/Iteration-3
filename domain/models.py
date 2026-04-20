class Product:
    def __init__(self, product_id, name, price):
        self.id = product_id
        self.name = name
        self.price = price


class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def subtotal(self):
        return self.product.price * self.quantity


class Order:
    def __init__(self, order_id):
        self.id = order_id
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def total(self):
        return sum(item.subtotal() for item in self.items)

    def print_order(self):
        for item in self.items:
            print(f"Item: {item.product.name} x{item.quantity} = ${item.subtotal():.2f}")
        print(f"Total = ${self.total():.2f}")
