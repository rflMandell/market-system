import sqlite3

def connect_database():
    conn = sqlite3.connect('products.db')
    return conn

def create_table():
    conn = connect_database()
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
        ''')
        conn.commit()
    finally:
        conn.close()

def authenticate_manager():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    if username == "admin" and password == "admin":
        return True
    else:
        print("Invalid credentials. Access denied.")
        return False

def search_product():
    conn = connect_database()
    try:
        cursor = conn.cursor()
        query = input("Enter the product ID or name (or 'exit' to cancel): ").strip()

        if query.lower() == "exit":
            print("Search canceled.")
            return None

        if query.isdigit():
            cursor.execute("SELECT * FROM products WHERE id = ?", (int(query),))
        else:
            cursor.execute("SELECT * FROM products WHERE name LIKE ? COLLATE NOCASE", (f"%{query}%",))

        product = cursor.fetchone()

        if product:
            print("\nProduct found:")
            print(f"ID: {product[0]}")
            print(f"Name: {product[1]}")
            print(f"Price: ${product[2]:.2f}")
            print(f"Quantity: {product[3]}")
            return product
        else:
            print("Product not found.")
            return None
    finally:
        conn.close()

def register_product():
    try:
        name = input("Enter the new product name:\n-> ").strip()
        price = float(input("Enter the new product price:\n-> "))
        quantity = int(input("Enter the new product quantity:\n-> "))

        conn = connect_database()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
            conn.commit()
            print("Product successfully registered!")
        finally:
            conn.close()
    except ValueError as e:
        print(f"Error: Invalid input. Ensure you enter numbers for price and quantity. Details: {e}")

def add_quantity():
    product = search_product()
    if product:
        try:
            quantity = int(input("Enter the quantity to be added:\n-> "))
            if quantity > 0:
                conn = connect_database()
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE products SET quantity = quantity + ? WHERE id = ?", (quantity, product[0]))
                    conn.commit()
                    cursor.execute("SELECT quantity FROM products WHERE id = ?", (product[0],))
                    new_quantity = cursor.fetchone()[0]
                    print(f"Quantity successfully updated! New quantity: {new_quantity}")
                finally:
                    conn.close()
            else:
                print("Error: Quantity must be greater than zero.")
        except ValueError:
            print("Error: Invalid input. Ensure you enter an integer.")

def checkout():
    cart = []
    while True:
        print("\n--- Checkout Mode ---")
        print("1 - Add product to cart")
        print("2 - View cart")
        print("3 - Finalize purchase")
        print("4 - Cancel purchase")
        option = input("Choose an option: ").strip()

        if option == "1":
            product = search_product()
            if product is not None:
                try:
                    quantity = int(input(f"Enter the quantity of '{product[1]}' to purchase: "))
                    if quantity <= product[3]:
                        cart.append({"name": product[1], "price": product[2], "quantity": quantity})
                        conn = connect_database()
                        try:
                            cursor = conn.cursor()
                            cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity, product[0]))
                            conn.commit()
                        finally:
                            conn.close()
                        print(f"{quantity} units of '{product[1]}' added to the cart.")
                    else:
                        print(f"Insufficient stock. Only {product[3]} units available.")
                except ValueError:
                    print("Error: Invalid input. Ensure you enter an integer.")

        elif option == "2":
            if not cart:
                print("The cart is empty.")
            else:
                print("\n--- Shopping Cart ---")
                for item in cart:
                    print(f"{item['quantity']} x {item['name']} - ${item['price']:.2f} each")
                print("--------------------------")

        elif option == "3":
            if not cart:
                print("The cart is empty. Nothing to finalize.")
            else:
                print("\n--- Finalizing Purchase ---")
                total = sum(item["price"] * item["quantity"] for item in cart)
                print(f"Total: ${total:.2f}")
                print("Purchase successfully completed!")
                cart.clear()
                break

        elif option == "4":
            print("Purchase canceled. All items removed from cart.")
            cart.clear()
            break

        else:
            print("Invalid option. Try again.")

def menu(role):
    while True:
        print("\nChoose an option:")
        if role == "manager":
            print("1 - Search Product")
            print("2 - Checkout")
            print("3 - Register Product")
            print("4 - Add Quantity")
        elif role == "employee":
            print("1 - Search Product")
            print("2 - Checkout")
        
        option = input("Enter the option number: ").strip()
        
        if option == "1":
            search_product()
        elif option == "2":
            checkout()
        elif option == "3" and role == "manager":
            if authenticate_manager():
                register_product()
        elif option == "4" and role == "manager":
            if authenticate_manager():
                add_quantity()
        else:
            print("Invalid option or insufficient permission. Try again.")

if __name__ == "__main__":
    create_table()
    while True:
        user_role = input("Enter your role (manager/employee): ").lower()
        if user_role in ["manager", "employee"]:
            break
        else:
            print("Invalid role. Enter 'manager' or 'employee'.")
    menu(user_role)