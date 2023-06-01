import sqlite3
import time
import serial
from functions import Card, play_audio, products
import sys

conn = sqlite3.connect('db.db')

card1 = ("ba6cc043", 500,  0)
card2 = ("daafdc73", 500,  0)

timestamp = time.time()

conn.execute('''CREATE TABLE IF NOT EXISTS cards (
  id STRING PRIMARY KEY,
  amount REAL,
  points INTEGER
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  card STRING,
  amount REAL,
  points INTEGER,
  product INTEGER
);''')
conn.execute('''CREATE TABLE IF NOT EXISTS topups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  card STRING,
  amount REAL
);''')
conn.commit()

#insert

# conn.execute("INSERT INTO cards VALUES (?, ?, ?)", card1)
# conn.execute("INSERT INTO cards VALUES (?, ?, ?)", card2)

# conn.commit()

cursor = conn.cursor()
# cursor.execute("SELECT * FROM cards")

# Fetch all rows from the result
# rows = cursor.fetchall()

# Process the fetched data
# for row in rows:
#     card_id, amount, points = row
#     print(f"Card ID: {card_id}, Amount: {amount}, Points: {points}")
    

ser = serial.Serial('COM13', 9600)

# read data from serial
while True:
    line = ser.readline().decode('utf-8').strip()
    print(line)
    
    if "uid" in line:
        card_id = line.split(':')[1]
        card = Card(cursor=cursor, card_id=card_id)
        conn.commit()
        
        print("\n\nOPTIONS\n************\n1 Card Information\n2 Buy Products\n3 Top Up\n4 Exit\n")
        play_audio("menu")
        choice = int(input("enter your choice: "))
        data = b""
        while choice != 4:
            if choice == 1:
                card.display()
                data = f"{card.balance}|{card.points}".encode()
            elif choice == 2:
                for product_id, product_details in products.items():
                    name = product_details["name"]
                    price = product_details["price"]
                    points = product_details["points"]
                    print(f"Product ID: {product_id}, Name: {name}, Price: {price}, Points: {points} \n")
                
                product_id = int(input("Enter the product number to buy it: "))
                card.buy(product_id=product_id)
                conn.commit()
                card.display()
                play_audio("purchased")
                data = f"{card.balance}|{card.points}".encode()
            
            elif choice == 3:
                amount = int(input("\n Enter Amount To Top Up: "))
                card.top_up(amount=amount)
                conn.commit()
                card.display()
                play_audio("topup")
                data = f"{card.balance}|{card.points}".encode()
                
            elif choice == 4:
                break
            else:
                print("\n\nInvalid choice . . . .")
                
            if data != b"":
                # print(data)
                ser.write(data)
                   
            choice = int(input("\n\nOPTIONS\n************\n1 Card Information\n2 Buy Products\n3 Top Up\n4 Exit\n enter your choice: "))
        
        a = input("Continue (y/n): ")
        a = a.lower()
        if a == 'y':
            continue
        else:
            break

    
        
        
        
        





