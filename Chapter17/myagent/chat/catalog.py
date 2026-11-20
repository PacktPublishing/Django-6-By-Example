"""Looks up the tea shop's products. The assistant calls these functions as tools.

The catalog is the JSON file at settings.TEA_SHOP_CATALOG, read on every call
so edits to it apply without a restart. The model reads each function's
docstring and type hints to decide when and how to call it.
"""

import json
from typing import Any

from django.conf import settings

SUMMARY_FIELDS = ("id", "name", "category", "price_eur", "unit", "caffeine", "flavor_notes")
MAX_ALTERNATIVES = 5


def load_products():
    """Return every product in the catalog."""
    with open(settings.TEA_SHOP_CATALOG, encoding="utf-8") as file:
        return json.load(file)["products"]


def summarize(product):
    """Return the fields needed to list a product, plus whether it can be bought now."""
    summary = {field: product[field] for field in SUMMARY_FIELDS}
    summary["in_stock"] = product["stock"] > 0
    return summary


def find_product(products, name_or_id):
    """Return the product with this id or name, or the only one whose name contains it."""
    key = name_or_id.strip().lower()
    for product in products:
        if key in (product["id"], product["name"].lower()):
            return product
    matches = [product for product in products if key in product["name"].lower()]
    return matches[0] if len(matches) == 1 else None


def search_text(product):
    """Return the lowercase text a keyword search looks in."""
    parts = [product["name"], product["category"], product["origin"], product["description"], *product["flavor_notes"]]
    return " ".join(parts).lower()


def search_products(
    query: str | None = None,
    category: str | None = None,
    caffeine: str | None = None,
    max_price_eur: float | None = None,
    in_stock_only: bool = False,
) -> list[dict[str, Any]]:
    """Search the shop's teas and accessories. Call with no arguments to list everything.

    Args:
        query: Keywords matched against name, origin, description and flavor notes,
            for example "smoky", "citrus vanilla" or "japan". Best matches come first.
        category: One of green, matcha, black, oolong, white, herbal, rooibos, accessory.
        caffeine: One of none, low, medium, high. Accessories have no caffeine level.
        max_price_eur: Only products costing at most this many euros.
        in_stock_only: Leave out products that are sold out.
    """
    words = query.lower().split() if query else []
    results = []
    for product in load_products():
        if category and product["category"] != category.lower():
            continue
        if caffeine and product["caffeine"] != caffeine.lower():
            continue
        if max_price_eur is not None and product["price_eur"] > max_price_eur:
            continue
        if in_stock_only and product["stock"] <= 0:
            continue
        text = search_text(product)
        score = sum(word in text for word in words)
        if words and not score:
            continue
        results.append((score, product))
    results.sort(key=lambda result: -result[0])
    return [summarize(product) for _, product in results]


def get_product(name_or_id: str) -> dict[str, Any]:
    """Return every detail of one product: description, origin, brewing advice and stock left.

    Args:
        name_or_id: The product's id, full name, or a distinctive part of its name.
    """
    product = find_product(load_products(), name_or_id)
    if product is None:
        return {"found": False, "message": f"No product named {name_or_id!r}. Use search_products to look around."}
    return {"found": True, **product, "in_stock": product["stock"] > 0}


def find_alternatives(
    product: str,
    category: str | None = None,
    flavor_notes: list[str] | None = None,
) -> dict[str, Any]:
    """Suggest in-stock products to offer instead of one that is sold out or not sold here.

    Args:
        product: Name or id of the product the customer asked for. It may not be in the catalog.
        category: Category to look in, needed when the product is not in the catalog
            (for example "white" for jasmine silver needle, "accessory" for a kettle).
        flavor_notes: Flavors the customer is after, needed when the product is not in the catalog
            (for example ["citrus", "floral"] for an Earl Grey).
    """
    products = load_products()
    requested = find_product(products, product)
    if requested is not None:
        category = category or requested["category"]
        flavor_notes = flavor_notes or requested["flavor_notes"]
    wanted_notes = {note.lower() for note in flavor_notes or []}

    scored = []
    for candidate in products:
        if candidate is requested or candidate["stock"] <= 0:
            continue
        score = len(wanted_notes & set(candidate["flavor_notes"]))
        if category and candidate["category"] == category.lower():
            score += 2
        if not score:
            continue
        # A matching caffeine level breaks ties but is not enough on its own.
        if requested is not None and requested["caffeine"] and candidate["caffeine"] == requested["caffeine"]:
            score += 1
        scored.append((score, candidate))
    scored.sort(key=lambda result: -result[0])

    return {
        "requested": summarize(requested) if requested is not None else None,
        "sold_here": requested is not None,
        "alternatives": [summarize(candidate) for _, candidate in scored[:MAX_ALTERNATIVES]],
    }


def list_categories() -> list[dict[str, Any]]:
    """Give an overview of the shop: each category with its number of products, how many are in stock, and prices."""
    categories = {}
    for product in load_products():
        entry = categories.setdefault(
            product["category"],
            {"category": product["category"], "products": 0, "in_stock": 0, "prices_eur": []},
        )
        entry["products"] += 1
        entry["in_stock"] += product["stock"] > 0
        entry["prices_eur"].append(product["price_eur"])
    for entry in categories.values():
        prices = entry.pop("prices_eur")
        entry["cheapest_eur"], entry["priciest_eur"] = min(prices), max(prices)
    return list(categories.values())


TOOLS = [search_products, get_product, find_alternatives, list_categories]
