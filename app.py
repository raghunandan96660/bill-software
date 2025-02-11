import sqlite3

class billing:
    def __init__(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect('billing.db')
        self.cursor = self.conn.cursor()

    def add_items(self):
        item = input('Enter the item: ')
        id = input('Enter id: ')
        stock = int(input('Enter the item count: '))
        price = int(input('Enter the item price: '))
        
        self.cursor.execute('INSERT INTO items (id, name, stock, price) VALUES (?, ?, ?, ?)', (id, item, stock, price))
        self.conn.commit()

    def updatePrice(self):
        while True:
            item_id = input('Enter item id or enter "e" to exit: ')
            if item_id == 'e':
                break
            price = int(input('Enter price: '))
            self.cursor.execute('UPDATE items SET price = ? WHERE id = ?', (price, item_id))
            self.conn.commit()

    def stock(self):
        print('--------------------------Stock--------------------------')
        print('   Item                                        Count')
        
        for row in self.cursor.execute('SELECT id, name, stock FROM items'):
            print(f'{row[1]:<40} {row[2]}')

    def updateStocks(self):
        while True:
            item_id = input('Enter item id or enter "e" to exit: ')
            if item_id == 'e':
                break
            count = int(input('Enter stock: '))
            self.cursor.execute('UPDATE items SET stock = stock + ? WHERE id = ?', (count, item_id))
            self.conn.commit()

    def order(self):
        product_list = set()
        product_count = {}
        
        while True:
            item_id = input('Add the order (enter the product id) or press "e" to exit: ')
            if item_id == 'e':
                break
            count = int(input('Enter the no of items: '))
            
            # Get current stock
            self.cursor.execute('SELECT stock FROM items WHERE id = ?', (item_id,))
            current_stock = self.cursor.fetchone()
            if current_stock and current_stock[0] >= count:
                product_count[item_id] = product_count.get(item_id, 0) + count
                self.cursor.execute('UPDATE items SET stock = stock - ? WHERE id = ?', (count, item_id))
                self.conn.commit()
            else:
                print(f'Insufficient stock for item id {item_id}')
        
        self.bill(product_list, product_count)

    def bill(self, product_list, product_count):
        total = 0
        header = (
            '-------------------------Invoice-----------------------------\n'
            '  Item       ItemCode       ItemPrice       ItemCount       ItemTotal  \n'
            '---------------------------------------------------------------------'
        )
        print(header)
        
        for item_id in product_count:
            self.cursor.execute('SELECT name, price FROM items WHERE id = ?', (item_id,))
            item_name, item_price = self.cursor.fetchone()
            count = product_count[item_id]
            item_total = count * item_price
            
            print(f'  {item_name:<10} {item_id:<12} {item_price:<12} {count:<12} {item_total:<12} rs  ')
            total += item_total
        
        footer = (
            '---------------------------------------------------------------------\n'
            f' Total =                                    {total} rs'
        )
        print(footer)

# Initialize the class and menu
n = billing()

while True:
    print('1. Stocks        |          2. Sells')
    choice = int(input())
    if choice == 1:
        print('--------------Stock Management-----------------')
        while True:
            print('1. Add items')
            print('2. Update prices')
            print('3. Update stock')
            print('4. View current stock')
            print('Enter 0 for exit')
            selection = int(input('Enter choice: '))
            if selection == 1:
                print('-------------Add Items-------------')
                n.add_items()
            elif selection == 2:
                print('-------------Update Prices-------------')
                n.updatePrice()
            elif selection == 3:
                print('-------------Update Stocks-------------')
                n.updateStocks()
            elif selection == 4:
                print('-------------Stocks-------------')
                n.stock()
            elif selection == 0:
                break        
    else:
        print('-------------Order----------------')
        n.order()
