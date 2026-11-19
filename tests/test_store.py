from store import catalog, cart, checkout


def test_catalog_product():
    r = catalog.app.test_client().get("/products/p1")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Laptop"


def test_catalog_unknown():
    assert catalog.app.test_client().get("/products/zzz").status_code == 404


def test_cart_add():
    c = cart.app.test_client()
    c.post("/cart/ana/add/p1/2")
    assert c.get("/cart/ana").get_json()["items"] == {"p1": 2}


def test_checkout_total(monkeypatch):
    def fake_fetch(url):
        if "/cart/" in url:
            return {"items": {"p1": 1, "p2": 2}}
        return {"price": 900.0 if url.endswith("p1") else 25.0}
    monkeypatch.setattr(checkout, "fetch", fake_fetch)
    r = checkout.app.test_client().get("/checkout/ana")
    assert r.get_json()["total"] == 1045.0