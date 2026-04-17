from domain.models import Order, OrderItem


class OrderService:
    def __init__(self, product_repo, order_repo):
        self.product_repo = product_repo
        self.order_repo = order_repo

    # REQUIRED: create_order(items_data)
    def create_order(self, items_data):
        order_id = len(self.order_repo.list_all()) + 1
        order = Order(order_id)

        # retrieve + validate + create
        for product_id, quantity in items_data:
            product = self.product_repo.get(product_id)

            if not product:
                print(f"Product {product_id} not found")
                continue

            if quantity <= 0:
                print("Invalid quantity")
                continue

            order.add_item(OrderItem(product, quantity))

        # save
        self.order_repo.save(order)
        return order

    
    def get_order(self, order_id):
        return self.order_repo.get(order_id)

   
    def get_order_total(self, order_id):
        order = self.order_repo.get(order_id)
        if not order:
            return 0
        return order.get_total()
