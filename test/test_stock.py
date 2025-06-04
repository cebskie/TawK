# tests/test_stock.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
