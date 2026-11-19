import os, json, urllib.request
from flask import Flask, jsonify

app = Flask(__name__)

CATALOG_URL = os.getenv("CATALOG_URL", "http://localhost:8001")
CART_URL = os.getenv("CART_URL", "http://localhost:8002")
TAX_RATE = 0.10  # flat 10% for the demo


def fetch(url):
    with urllib.request.urlopen(url, timeout=3) as r:
        return json.loads(r.read())


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/checkout/<user>")
def checkout(user):
    try:
        items = fetch(f"{CART_URL}/cart/{user}")["items"]
        if not items:
            return jsonify(error="Cart is empty"), 400
        lines, subtotal = [], 0.0
        for pid, qty in items.items():
            price = fetch(f"{CATALOG_URL}/products/{pid}")["price"]
            lines.append({"product": pid, "qty": qty, "line_total": price * qty})
            subtotal += price * qty
    except Exception:
        return jsonify(error="Upstream service unavailable"), 503
    tax = round(subtotal * TAX_RATE, 2)
    return jsonify(user=user, lines=lines, subtotal=subtotal,
                   tax=tax, total=round(subtotal + tax, 2))