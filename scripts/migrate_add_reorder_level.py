"""
Safe migration: add reorder_level column to products if it doesn't exist
and set default values for existing products.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'Data', 'database.db')
DB_PATH = os.path.abspath(DB_PATH)

def column_exists(conn, table, column):
    cur = conn.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cur.fetchall()]
    return column in cols


def add_reorder_level():
    print('Opening DB:', DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    try:
        if not column_exists(conn, 'products', 'reorder_level'):
            print('Adding reorder_level column to products...')
            conn.execute('ALTER TABLE products ADD COLUMN reorder_level INTEGER DEFAULT 5')
            conn.commit()
            print('Column added.')
        else:
            print('Column reorder_level already exists.')

        # Ensure no NULLs and set sensible default where NULL
        cur = conn.execute('SELECT COUNT(*) FROM products WHERE reorder_level IS NULL')
        null_count = cur.fetchone()[0]
        if null_count:
            print(f'Setting reorder_level=5 for {null_count} existing rows where NULL...')
            conn.execute('UPDATE products SET reorder_level = 5 WHERE reorder_level IS NULL')
            conn.commit()
            print('Updated NULL reorder_level values to 5.')
        else:
            print('No NULL reorder_level values found.')

        # For safety, show a sample of products with reorder_level
        print('\nSample products with reorder_level:')
        for row in conn.execute('SELECT id, name, qty, reorder_level FROM products ORDER BY id LIMIT 20'):
            print(row)

    finally:
        conn.close()

if __name__ == '__main__':
    add_reorder_level()
