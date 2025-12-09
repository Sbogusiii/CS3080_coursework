import random
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import string

# generation functions

def generate_fake_name():
    first_names = [
        "James", "Mary", "Robert", "Patricia", "Michael", "Jennifer", 
        "William", "Linda", "David", "Elizabeth", "Joseph", "Barbara", 
        "Richard", "Susan", "Charles", "Jessica", "Thomas", "Sarah", 
        "Daniel", "Karen", "Christopher", "Nancy", "Matthew", "Lisa",
        "Andrew", "Betty", "Joshua", "Sandra", "Kevin", "Helen",
        "Brian", "Ashley", "George", "Donna", "Timothy", "Carol"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", 
        "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", 
        "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", 
        "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
        "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
        "Walker", "Young", "Allen", "King", "Wright", "Scott"
    ]
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    
    return f"{first} {last}".upper()

def generate_fake_email(name):
    # generates fake email (nameXXX@gmail.com) from cardholder name.
    parts = name.lower().split()
    
    if len(parts) >= 2:
        username_base = f"{parts[0]}.{parts[-1]}"
    else:
        username_base = parts[0] if parts else "user"
        
    rand_num = random.randint(10, 999)
    return f"{username_base}{rand_num}@gmail.com"

def generate_random_password(length, has_symbols=True):
    # generates password ensuring mixed case, digits, and optionally symbols.
    
    # define character sets
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    
    # base characters always included
    all_chars = lower + upper + digits
    
    # guarantees list starts with one of each of our basic chars (mixed case + digit)
    guarantee_list = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
    ]

    if has_symbols:
        all_chars += symbols
        guarantee_list.append(random.choice(symbols))
    
    # ensures min length for guaranteed complexity
    if length < len(guarantee_list):
        length = 8
        
    # fills rest of password length randomly
    password = guarantee_list + [random.choice(all_chars) for _ in range(length - len(guarantee_list))]
    
    # shuffles list to randomize character positions
    random.shuffle(password)
    
    return "".join(password)

# core card generation-

def generate_card_number(card_type):
    # generates dummy credit card numbers based on card type rules and returns it formatted (4-6-5 for Amex, else, 4-4-4-4).
    card_rules = {
        "Visa": {"prefix": ["4"], "length": 16},
        "Mastercard": {"prefix": [str(i) for i in range(51, 56)], "length": 16},
        "Amex": {"prefix": ["34", "37"], "length": 15},
        "Discover": {"prefix": ["6011", "644", "65"], "length": 16},
    }

    rules = card_rules.get(card_type)
    if not rules:
        return None

    prefix = random.choice(rules["prefix"])
    remaining_length = rules["length"] - len(prefix)
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(remaining_length)])
    raw_card_number = prefix + random_digits
    
    if rules["length"] == 16:
        return f"{raw_card_number[:4]} {raw_card_number[4:8]} {raw_card_number[8:12]} {raw_card_number[12:]}"
    elif rules["length"] == 15:
        return f"{raw_card_number[:4]} {raw_card_number[4:10]} {raw_card_number[10:]}"
    
    return raw_card_number 

def generate_expiration_date():
    # generates expiration date between 2 and 5 years
    now = datetime.datetime.now()
    year_offset = random.randint(2, 5)
    exp_year = now.year + year_offset
    exp_month = random.randint(1, 12)
    
    return f"{exp_month:02d}/{str(exp_year)[2:]}"

def generate_cvv(card_type):
    # enerates a CVV (3 digits) or CID (4 digits for Amex)
    if card_type == "Amex":
        return ''.join([str(random.randint(0, 9)) for _ in range(4)])
    else:
        return ''.join([str(random.randint(0, 9)) for _ in range(3)])

# Tkinter GUI

class CardGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Dummy User/Card Generator")

        # variables
        self.card_type_var = tk.StringVar(master)
        self.name_var = tk.StringVar(master)
        self.password_length_var = tk.StringVar(master) 
        self.has_symbols_var = tk.BooleanVar(master, value=True)
        
        self.card_type_var.set("Visa")
        self.password_length_var.set("12") 

        # setup main frame
        main_frame = ttk.Frame(master, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # input section
        
        # card type
        ttk.Label(main_frame, text="Select Card Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        card_types = ["Visa", "Mastercard", "Amex", "Discover"]
        card_type_dropdown = ttk.OptionMenu(main_frame, self.card_type_var, "Visa", *card_types)
        card_type_dropdown.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # cardholder name
        ttk.Label(main_frame, text="Cardholder Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # password length
        ttk.Label(main_frame, text="Password Length:").grid(row=2, column=0, sticky=tk.W, pady=5)
        password_lengths = ["8", "12", "16", "20"]
        length_dropdown = ttk.OptionMenu(main_frame, self.password_length_var, "12", *password_lengths)
        length_dropdown.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # has symbols checkbox
        has_symbols_check = ttk.Checkbutton(main_frame, text="Include Symbols (e.g., !@#$)", variable=self.has_symbols_var)
        has_symbols_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5) 

        # separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10) 

        # generate button
        generate_button = ttk.Button(main_frame, text="Generate User & Card", command=self.generate_and_display)
        generate_button.grid(row=5, column=0, columnspan=2, pady=15)
        
        # separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10) 

        # output
        ttk.Label(main_frame, text="✨ New User/Card Info:").grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        labels = ["Name:", "Email:", "Password:", "SEPARATOR", "Card Type:", "Card #:", "Expiration Date:", "CVV/CID:"]
        self.result_vars = {}

        output_row_start = 8 

        for i, label_text in enumerate(labels):
            current_row = i + output_row_start
            
            if label_text == "SEPARATOR":
                # separator #2
                ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=current_row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
                continue

            # label 
            ttk.Label(main_frame, text=label_text, font=('Arial', 10, 'bold')).grid(row=current_row, column=0, sticky=tk.W, pady=2)
            
            # placeholder for result
            result_var = tk.StringVar(master)
            self.result_vars[label_text] = result_var
            
            ttk.Label(main_frame, textvariable=result_var, font=('Courier New', 10)).grid(row=current_row, column=1, sticky=tk.W, pady=2)


    def generate_and_display(self):
        
        card_type = self.card_type_var.get()
        name_input = self.name_var.get().strip()
        length = int(self.password_length_var.get()) 
        has_symbols = self.has_symbols_var.get()
        
        # 1. name (inputed or generated)
        if not name_input:
            name = generate_fake_name()
        else:
            name = name_input.upper() 

        # generate new user credentials
        email = generate_fake_email(name)
        # pass symbols option to password generator
        password = generate_random_password(length, has_symbols) 
        
        # generate card components
        card_number = generate_card_number(card_type)
        exp_date = generate_expiration_date()
        cvv = generate_cvv(card_type)

        # update the result labels
        self.result_vars["Name:"].set(name)
        self.result_vars["Email:"].set(email)
        self.result_vars["Password:"].set(password)
        self.result_vars["Card Type:"].set(card_type)
        self.result_vars["Card #:"].set(card_number)
        self.result_vars["Expiration Date:"].set(exp_date)
        self.result_vars["CVV/CID:"].set(cvv)


if __name__ == '__main__':
    root = tk.Tk()
    app = CardGeneratorApp(root)
    root.mainloop()