import sqlite3
import pygame


products = {
    1: {"name": "laptop", "price": 1000, "points": 50},
    2: {"name": "smartphone", "price": 800, "points": 40},
    3: {"name": "headphones", "price": 100, "points": 5},
    4: {"name": "pizza", "price": 10, "points": 2},
    5: {"name": "hamburger", "price": 5, "points": 5},
    6: {"name": "ice cream", "price": 3, "points": 1},
    7: {"name": "t-shirt", "price": 20, "points": 10},
    8: {"name": "jeans", "price": 50, "points": 6},
    9: {"name": "shoes", "price": 80, "points":5 },
}

def get_product(product_id):
    product_details = products.get(product_id)

    return product_details
    

def play_audio(option):
    pygame.init()

    mp3_file = "audio/"
    
    if option == "menu":
        mp3_file += "menu.mp3"
    elif option == "purchased":
        mp3_file += "purchased.mp3"
    elif option == "topup":
        mp3_file += "topup.mp3"

    # Set the desired volume (optional)
    volume = 0.8  # Value between 0.0 and 1.0

    # Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(mp3_file)

    # Set the volume
    pygame.mixer.music.set_volume(volume)

    # Play the MP3 file
    pygame.mixer.music.play()

    # Wait for the MP3 to finish playing (optional)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Quit pygame
    pygame.quit()
    
    
class Card:
    def __init__(self, cursor:sqlite3.Cursor, card_id):
        self.balance = 0
        self.points = 0
        self.cursor = cursor
        self.card_id = card_id
        
        cursor.execute("SELECT * FROM cards where id = ?", (card_id,))
        card_info = cursor.fetchone()
        
        if not card_info:
            cursor.execute("INSERT INTO cards VALUES (?, ?, ?)", (self.card_id, 0, 0))
            print("The card is not registered so it is now registed with 0$ and 0 points")
            
        else:
            _id, amount, points = card_info
            self.balance = amount
            self.points = points
    
    def display(self):
        print("\n\nCARD INFORMATION:")
        print("__________________") 
        print(f"UID: {self.card_id}")
        print(f"Balance: {self.balance}")
        print(f"Points: {self.points}\n\n")
        
    def buy(self, product_id):
        product = get_product(product_id)
        amount = product["price"]
        points = product["points"]
        
        if self.balance > amount:    
            cursor = self.cursor
            cursor.execute("UPDATE cards SET amount=?, points=? where id=?", (self.balance - amount, self.points + points,  self.card_id))
            cursor.execute("INSERT INTO transactions (card, amount, points, product) VALUES(?, ?, ?, ?)", (self.card_id, amount, points, product_id))
            self.balance -= amount
            self.points += points
            print(f"Purchase successful. Remaining balance: {self.balance}")
        else:
            print("Insufficient balance. Please top up.")

    def top_up(self, amount):
        cursor  = self.cursor
        cursor.execute("UPDATE cards SET amount=? WHERE id=?", (self.balance + amount, self.card_id))
        cursor.execute("INSERT INTO topups (card, amount) VALUES (?, ?)", (self.card_id, amount))
        self.balance += amount
        print(f"Top-up successful. Current balance: {self.balance}")
