from flask import Flask, jsonify

app = Flask(__name__)
CARTS = {}


@app.route("/cart/<user>")
def show(user):
    return jsonify(user=user, items=CARTS.get(user, {}))


@app.route("/cart/<user>/add/<pid>/<int:qty>", methods=["POST"])
def add(user, pid, qty):
    if qty <= 0:
        return jsonify(error="Quantity must be positive"), 400
    cart = CARTS.setdefault(user, {})
    cart[pid] = cart.get(pid, 0) + qty
    return jsonify(user=user, items=cart)