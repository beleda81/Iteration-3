from flask import Flask, jsonify
from flask import request
from flask import render_template

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


@app.route("/orders", methods=["GET"])
def get_orders():
    orders = o_repo.list_all()

    result = []
    for o in orders:
        result.append({
            "order_id": o.id
        })

    return jsonify(result)

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    try:
        order = service.create_order(data)
        return jsonify({"message": "Order created", "order_id": order.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    try:
        product = Product(data["id"], data["name"], data["price"])
        p_repo.add(product)

        return jsonify({"message": "Product created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = o_repo.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    del o_repo.orders[order_id]

    return jsonify({"message": "Order deleted"})


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = p_repo.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    del p_repo.products[product_id]

    return jsonify({"message": "Product deleted"})

# Run the App
if __name__ == "__main__":
    app.run(debug=True)
