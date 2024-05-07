from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Create a basic SQLite database for storing tickets
def init_db():
    with sqlite3.connect('retail_management.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS items
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         name TEXT, 
                         price REAL, 
                         quantity INTEGER)''')

@app.route('/')
def home():
    # Fetch all tickets from the database
    with sqlite3.connect('retail_management.db') as conn:
        items = conn.execute('SELECT * FROM items').fetchall()
    return render_template('retail.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    with sqlite3.connect('retail_management.db') as conn:
        conn.execute('INSERT INTO items (name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
    return 'Item added successfully!'

@app.route('/update', methods=['POST'])
def update_item():
    item_id = int(request.form['id'])
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    with sqlite3.connect('retail_management.db') as conn:
        conn.execute('UPDATE items SET name = ?, price = ?, quantity = ? WHERE id = ?', (name, price, quantity, item_id))
    return 'Item updated successfully!'

@app.route('/delete', methods=['POST'])
def delete_item():
    item_id = int(request.form['id'])
    with sqlite3.connect('retail_management.db') as conn:
        conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    return 'Item deleted successfully!'

@app.route('/search', methods=['GET'])
def search_tickets():
    search_query = request.args.get('query', '')
    try:
        search_query = int(search_query)  # Try converting query to an integer (item ID)
        with sqlite3.connect('retail_management.db') as conn:
            result = conn.execute('SELECT * FROM items WHERE id = ?', (search_query,)).fetchone()
        if result:
            # item found, render template with ticket details
            return render_template('retail.html', items=[result])
        else:
            # item not found, render template with message
            return render_template('retail.html', not_found=True)
    except ValueError:
        # Invalid input (not a valid integer), render template with message
        return render_template('retail.html', not_found=True)



if __name__ == '__main__':
    init_db()
    app.run(port=5012) 
