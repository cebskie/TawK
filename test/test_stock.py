# tests/test_db.py
from core.db import fetch_categories, fetch_products_by_category, fetch_product_details

def test_fetch_categories():
    result = fetch_categories()
    assert isinstance(result, list)

def test_fetch_products_by_category():
    result = fetch_products_by_category("Cameras & Photography")  # Ganti sesuai nama kategori real
    assert isinstance(result, list)

def test_fetch_product_details():
    result, columns = fetch_product_details("Compact 4K Vlogging Camera")  # Ganti sesuai nama produk real
    assert isinstance(result, list)
    assert isinstance(columns, list)
