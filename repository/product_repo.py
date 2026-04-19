class ProductRepository:
    def __init__(self):
        self.products = {}

    def add(self, product):
        self.products[product.id] = product

    def get(self, product_id):
        return self.products.get(product_id)

    def list_all(self):
        return list(self.products.values())