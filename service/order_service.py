from domain.models import Order, OrderItem


class OrderService:
    def __init__(self, product_repo, order_repo):
        self.product_repo = product_repo
        self.order_repo = order_repo


    def create_order(self, items_data):

        if not items_data:
            raise ValueError("Order must contain at least one item")

        order_id = len(self.order_repo.list_all()) + 1
        order = Order(order_id)

        # retrieve + validate + create
        for item in items_data:
            if isinstance(item, dict):
                product_id = item["id"]
                quantity = item["qty"]
            else:  # assume tuple
                product_id, quantity = item

            product = self.product_repo.get(product_id)


            if not product:
                raise ValueError(f"Product {product_id} not found")


            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0")

            order.add_item(OrderItem(product, quantity))

        # save
        self.order_repo.save(order)
        return order


    def get_order(self, order_id):
        order = self.order_repo.get(order_id)

        if not order:
            raise ValueError("Order not found")

        return order


    def get_order_total(self, order_id):
        order = self.get_order(order_id)
        return order.total()
