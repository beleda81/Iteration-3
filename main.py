from domain.models import Product
from repository.product_repo import ProductRepository
from repository.order_repo import OrderRepository
from service.order_service import OrderService


def main():
    # repositories
    product_repo = ProductRepository()
    order_repo = OrderRepository()

    # service
    order_service = OrderService(product_repo, order_repo)

    # add products
    product_repo.add(Product(1, "Mug", 12.50))
    product_repo.add(Product(2, "Scarf", 25.00))

    # format
    items = [
        {"id": 1, "qty": 2},
        {"id": 2, "qty": 1}
    ]

    # create order
    order = order_service.create_order(items)

    # retrieve + print
    order = order_service.get_order(order.id)
    order.print_order()

    # total
    total = order_service.get_order_total(order.id)
    print(f"Total = ${total:.2f}")


if __name__ == "__main__":
    main()
