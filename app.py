from flask import Flask, jsonify

from domain.models import Product
from repository.product_repo import ProductRepository
from repository.order_repo import OrderRepository
from service.order_service import OrderService


app = Flask(__name__)



# Initialize Repositories & Service
p_repo = ProductRepository()
o_repo = OrderRepository()
service = OrderService(p_repo, o_repo)



# Seed Data
def startup_data():
    p_repo.add(Product(1, "Mug", 12.50))
    p_repo.add(Product(2, "Scarf", 25.00))


def startup_order():
    items = [
        {"id": 1, "qty": 2},
        {"id": 2, "qty": 1}
    ]
    service.create_order(items)


# Run seed functions
startup_data()
startup_order()



# Routes
@app.route("/products", methods=["GET"])
def get_products():
    products = p_repo.list_all()

    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "price": p.price
        })

    return jsonify(result)


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    try:
        order = service.get_order(order_id)
        total = service.get_order_total(order_id)

        items = []
        for item in order.items:
            items.append({
                "product": item.product.name,
                "quantity": item.quantity,
                "subtotal": item.subtotal()
            })

        return jsonify({
            "order_id": order.id,
            "items": items,
            "total": total
        })

    except ValueError:
        return jsonify({"error": "Order not found"}), 404



# Run the App
if __name__ == "__main__":
    app.run(debug=True)
