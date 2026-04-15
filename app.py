



# start up test data
def startup_data():
    p_repo.add_product(Product(1, "Mug", 12.50))
    p_repo.add_product(Product(2, "Scarf", 25.00))

startup_data()

# start up order test data
def startup_order():
    items = [
        {"id": 1, "qty": 2},
        {"id": 2, "qty": 1}
    ]
    service.create_order(items)

startup_order()