# Product Manager

This project is a simple product management system using SQLite3 in Python. It allows authenticated users as "manager" or "employee" to perform various operations on a product database.

## Features

- **Create database and product table** automatically on startup.
- **Search for products** by ID or name.
- **Register new products** (only for "manager").
- **Add quantity to an existing product** (only for "manager").
- **Checkout mode**, allowing products to be added to the cart and purchases to be finalized.
- **Basic authentication** for managers before certain operations.

## Technologies Used

- **Python 3**
- **SQLite3** (built-in local database)

## How to Run the Project

1. Make sure you have Python installed on your system.
2. Download the source code file.
3. Run the script in the terminal or command prompt:
   ```bash
   python filename.py
   ```
4. Enter your role when prompted ("manager" or "employee").

## Code Structure

- `connect_database()`: Establishes a connection with the database.
- `create_table()`: Creates the product table if it does not exist.
- `authenticate_manager()`: Requests administrator credentials.
- `search_product()`: Allows searching for a product by ID or name.
- `register_product()`: Adds a new product to the database.
- `add_quantity()`: Increases the stock of an existing product.
- `checkout()`: Simulates a sales checkout with a shopping cart.
- `menu()`: Displays action options according to the user's role.

## Usage Example

When running the script, the user must enter their role:
```bash
enter your role (manager/employee):
```

If **manager**, they will be able to register products and add quantity. If **employee**, they will only have access to product search and checkout mode.

### Product Search
```bash
enter the ID or name of the item you want to search for:
```

### Product Registration (only "manager")
```bash
enter the name of the new product:
enter the price of the new product:
enter the quantity of the new product:
```

### Add Quantity (only "manager")
```bash
enter the quantity to be added:
```

### Checkout Mode
```bash
1 - add product to cart
2 - view cart
3 - finalize purchase
4 - cancel purchase
```

## Future Improvements
- Implementation of a more secure authentication system.
- Graphical interface for better usability.
- Support for multiple users with different permissions.

## License
This project is under the MIT license.
