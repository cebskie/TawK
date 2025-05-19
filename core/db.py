import mysql.connector

# Connect to DB

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='inventory'
    )


def fetch_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT c.cat_name
        FROM categories c
        JOIN products p ON c.cat_id = p.cat_id
    """)
    categories = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return categories


def fetch_products_by_category(category_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.prod_name
        FROM products p
        JOIN categories c ON p.cat_id = c.cat_id
        WHERE c.cat_name = %s
    """, (category_name,))
    products = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return products


def fetch_product_details(product_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.prod_name AS Product,
               p.stock_quantity AS 'Available Stock',
               p.price AS Price
        FROM products p
        JOIN categories c ON p.cat_id = c.cat_id
        WHERE p.prod_name = %s
    """, (product_name,))
    columns = [desc[0] for desc in cursor.description]
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result, columns
