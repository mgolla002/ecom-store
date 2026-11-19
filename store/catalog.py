from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = {
    "p1": {"name": "Laptop", "price": 900.0},
    "p2": {"name": "Mouse", "price": 25.0},
    "p3": {"name": "Headphones", "price": 120.0},
}


@app.route("/products")
def products():
    return jsonify(PRODUCTS)


@app.route("/products/<pid>")
def product(pid):
    item = PRODUCTS.get(pid)
    if not item:
        return jsonify(error="Product not found"), 404
    return jsonify(id=pid, **item)