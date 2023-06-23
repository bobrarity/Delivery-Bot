import sqlite3


def create_user_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        telegram_id BIGINT NOT NULL UNIQUE,
        phone TEXT,
        location TEXT
    );
    ''')
    database.commit()
    database.close()


def create_carts_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts(
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id) UNIQUE,
        total_price DECIMAL(12, 2) DEFAULT 0,
        total_products INTEGER DEFAULT 0
    );
    ''')
    database.commit()
    database.close()


def create_cart_products_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_products(
        cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER REFERENCES carts(cart_id),
        product_name VARCHAR(50) NOT NULL,
        quantity INTEGER NOT NULL,
        final_price DECIMAL(12, 2) NOT NULL,
        
        UNIQUE(cart_id, product_name)
    );
    ''')
    database.commit()
    database.close()


def create_categories_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(20) NOT NULL UNIQUE
    );
    ''')
    database.commit()
    database.close()


def create_history_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id BIGINT,
        history TEXT
    );
    ''')
    database.commit()
    database.close()


def insert_categories():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO categories(category_name) VALUES
    ('Lavash'),
    ('Burgers'),
    ('Hot-Dogs'),
    ('Pizza'),
    ('French fries'),
    ('Kebab'),
    ('Sauces'),
    ('Beverages'),
    ('Desserts')
    ''')
    database.commit()
    database.close()


def create_products_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        product_name VARCHAR(20) NOT NULL UNIQUE,
        price DECIMAL(12, 2) NOT NULL,
        description VARCHAR(100),
        image TEXT,
        FOREIGN KEY(category_id) REFERENCES categories(category_id)
    );
    ''')
    database.commit()
    database.close()


def insert_products_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO products(category_id, product_name, price, description, image) VALUES
    ('1', 'MINI LAVASH', 20000, 'Meat, tomatoes, dough', 'media/lavash/lavash_1.jpg'),
    ('1', 'LAVASH', 24000, 'Meat, tomatoes, dough', 'media/lavash/lavash_2.jpg'),
    ('1', 'CHEESE LAVASH', 28000, 'Meat, tomatoes, dough', 'media/lavash/lavash_3.jpg'),
    ('2', 'BURGER', 26000, 'Meat, tomatoes, bun', 'media/burger/burger_1.jpg'),
    ('2', 'CHEESE BURGER', 28000, 'Meat, tomatoes, bun, cheese', 'media/burger/burger_2.jpg'),
    ('2', 'DOUBLE BURGER', 32000, 'Double meat, tomatoes, bun', 'media/burger/burger_3.jpg'),
    ('3', 'HOT-DOG', 18000, 'Sausage, tomatoes, bun', 'media/hot-dog/hot-dog_1.jpg'),
    ('3', 'KING HOT-DOG', 26000, 'Sausage, tomatoes, bun', 'media/hot-dog/hot-dog_2.jpg'),
    ('4', 'PEPPERONI MIX', 66000, 'Pepper, onion, pepperoni sausage, meat, dough, cheese', 'media/pizza/pizza_1.jpg'),
    ('4', 'PEPPERONI', 56000, 'Cheese, pepperoni sausage, dough', 'media/pizza/pizza_2.jpg'),
    ('4', 'MIX', 56000, 'Cheese, pepperoni, chicken, onion, olive, dough', 'media/pizza/pizza_3.jpg'),
    ('5', 'FRENCH FRIES', 16000, 'Regular potato french fries', 'media/fri/fri_1.jpg'),
    ('5', 'CHEESE FRENCH FRIES', 22000, 'Cheese potato french fries', 'media/fri/fri_2.jpg'),
    ('6', 'KEBAB', 35000, 'Meat, onions, green', 'media/kebab/kebab_1.jpg'),
    ('6', 'KEBAB MIX 1', 72000, 'Meat, onions, green, cucumber, tomato, potato', 'media/kebab/kebab_2.jpg'),
    ('6', 'KEBAB MIX 2', 55000, 'Meat, sauce, green, pepper, tomato, rice', 'media/kebab/kebab_3.jpg'),
    ('7', 'GARLIC SAUCE', 3000, 'Garlic sauce', 'media/sauces/sauce_1.jpg'),
    ('7', 'CHEESE SAUCE', 3000, 'Cheese sauce', 'media/sauces/sauce_2.jpg'),
    ('7', 'BARBECUE SAUCE', 3000, 'Barbecue sauce', 'media/sauces/sauce_3.jpg'),
    ('8', 'COKE', 8000, 'Cold coke', 'media/beverages/water_1.jpg'),
    ('8', 'FANTA', 8000, 'Cold fanta', 'media/beverages/water_2.jpg'),
    ('8', 'SPRITE', 8000, 'Cold sprite', 'media/beverages/water_3.jpg'),
    ('9', 'BROWNIE', 16000, 'Chocolate brownie cake', 'media/desserts/dessert_1.jpg'),
    ('9', 'OREO CHEESECAKE', 24000, 'Milk oreo chocolate cheese cake', 'media/desserts/dessert_2.jpg'),
    ('9', 'CHOCO BISCUITS', 18000, 'Chocolate homemade cookies', 'media/desserts/dessert_3.jpg')
    ''')
    database.commit()
    database.close()


def first_select_user(chat_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE telegram_id = ?
    ''', (chat_id,))
    user = cursor.fetchone()
    database.close()
    return user


def first_register_user(chat_id, full_name):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name) VALUES (?, ?)
    ''', (chat_id, full_name))
    database.commit()
    database.close()


def update_user_to_finish_register(chat_id, phone):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users
    SET phone = ?
    WHERE telegram_id = ?
    ''', (phone, chat_id))
    database.commit()
    database.close()


def update_user_to_finish_register2(chat_id, location):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users
    SET location = ?
    WHERE telegram_id = ?
    ''', (location, chat_id))
    database.commit()
    database.close()


def insert_to_cart(chat_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO carts(user_id) VALUES
    (
        (SELECT user_id from users WHERE telegram_id = ?)
    )
    ''', (chat_id,))
    database.commit()
    database.close()


def get_all_categories():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM categories;
    ''')
    categories = cursor.fetchall()
    database.close()
    return categories


def get_products_by_category(category_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_id, product_name
    FROM products WHERE category_id = ?
    ''', (category_id,))
    products = cursor.fetchall()
    database.close()
    return products


def get_product_detail(product_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM products
    WHERE product_id = ?
    ''', (product_id,))
    product = cursor.fetchone()
    database.close()
    return product


def get_user_cart_id(chat_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_id FROM carts
    WHERE user_id = (
        SELECT user_id FROM users WHERE telegram_id = ?
    )
    ''', (chat_id,))
    cart_id = cursor.fetchone()[0]
    database.close()
    return cart_id


def insert_or_update_cart_product(cart_id, product_name, quantity, final_price):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    try:
        cursor.execute('''
        INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
        VALUES (?, ?, ?, ?)
        ''', (cart_id, product_name, quantity, final_price))
        database.commit()
        return True
    except:
        cursor.execute('''~
        UPDATE cart_products
        SET quantity = ?,
        final_price = ?
        WHERE product_name = ? AND cart_id = ?
        ''', (quantity, final_price, product_name, cart_id))
        database.commit()
        return False
    finally:
        database.close()


def update_total_products_total_price(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE carts
    SET total_products = (
        SELECT SUM(quantity) FROM cart_products
        WHERE cart_id = :cart_id
    ),
    total_price = (
        SELECT SUM(final_price) FROM cart_products
        WHERE cart_id = :cart_id
    )
    WHERE cart_id = :cart_id
    ''', {'cart_id': cart_id})
    database.commit()
    database.close()


def get_total_products_price(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT total_products, total_price FROM carts WHERE cart_id = ?;
    ''', (cart_id,))
    total_products, total_price = cursor.fetchone()
    database.close()
    return total_products, total_price


def get_cart_products(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name, quantity, final_price
    FROM cart_products
    WHERE cart_id = ? 
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products


def get_cart_products_for_delete(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_product_id, product_name
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products


def delete_cart_product_from_database(cart_product_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products WHERE cart_product_id = ?
    ''', (cart_product_id,))
    database.commit()
    database.close()


def get_user_info(chat_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT full_name, phone, location
    FROM users
    WHERE telegram_id = ?
    ''', (chat_id,))
    user_info = cursor.fetchall()
    database.close()
    return user_info


def edit_user_name(chat_id, new_name):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users
    SET full_name = ?
    WHERE telegram_id = ?
    ''', (new_name, chat_id))
    database.commit()
    database.close()


def edit_user_phone(chat_id, new_phone):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users
    SET phone = ?
    WHERE telegram_id = ?
    ''', (new_phone, chat_id))
    database.commit()
    database.close()


def clear_cart(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE carts
    SET total_price = 0, total_products = 0
    WHERE cart_id = ?
    ''', (cart_id, ))
    cursor.execute('''
    DELETE FROM cart_products WHERE cart_id = ?
    ''', (cart_id, ))
    database.commit()
    database.close()


# create_user_table()
# create_carts_table()
# create_cart_products_table()
# create_categories_table()
# create_history_table()
# insert_categories()
# create_products_table()
# insert_products_table()
