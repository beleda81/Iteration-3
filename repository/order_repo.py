class OrderRepository:
    def __init__(self):
        self.orders = {}

    def save(self, order):
        self.orders[order.id] = order

    def get(self, order_id):
        return self.orders.get(order_id)

    def list_all(self):
        return list(self.orders.values())