import random
import datetime

def generate_card_number(card_type):
    # card type prefixes and lengths
    # MII (Major Industry Identifier) and IIN (Issuer Identification Number)
    card_rules = {
        "Visa": {"prefix": ["4"], "length": 16},
        "Mastercard": {"prefix": [str(i) for i in range(51, 56)], "length": 16}, # 51-55
        "Amex": {"prefix": ["34", "37"], "length": 15},
        "Discover": {"prefix": ["6011", "644", "65"], "length": 16},
    }

    rules = card_rules.get(card_type)
    if not rules:
        return None

    # 1. choose prefix
    prefix = random.choice(rules["prefix"])
    
    # calculate how many digits are needed
    remaining_length = rules["length"] - len(prefix)
    
    # generate the random digits
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(remaining_length)])
    
    # combine and return
    card_number = prefix + random_digits
    
    # formats 16-digit "card" with spaces for readability
    if rules["length"] == 16:
        return f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
    
    return card_number

def generate_expiration_date():
    # get current date
    now = datetime.datetime.now()
    
    # randomly select offset (2-5 is standard according to google)
    year_offset = random.randint(2, 5)
    
    # calculate expiration year
    exp_year = now.year + year_offset
    
    # randomize month (1-12)
    exp_month = random.randint(1, 12)
    
    # format MM/YY
    return f"{exp_month:02d}/{str(exp_year)[2:]}"

def generate_cvv(card_type):
    if card_type == "Amex":
        # amex uses 4-digit CID
        return ''.join([str(random.randint(0, 9)) for _ in range(4)])
    else:
        # Visa, MC, Discover use 3-digit CVV
        return ''.join([str(random.randint(0, 9)) for _ in range(3)])

def main():
    print("== 💳 Dummy Credit Card Generator ==")
    
    # prompt for card yype
    valid_types = ["Visa", "Mastercard", "Amex", "Discover"]
    while True:
        card_type_input = input(f"Enter the card type you want ({'/'.join(valid_types)}): ").strip().capitalize()
        if card_type_input in valid_types:
            card_type = card_type_input
            break
        else:
            print("Invalid card type. Please choose from Visa, Mastercard, Amex, or Discover.")
            
    # prompt for name
    name = input("Enter the name for the card: ").strip().upper()
    if not name:
        name = "DUMMY INFO" # default if nothing is entered

    # generate card details
    card_number = generate_card_number(card_type)
    exp_date = generate_expiration_date()
    cvv = generate_cvv(card_type)

    # display results
    print("\n" + "="*40)
    print("✨ Here's your new dummy card info: ✨")
    print(f"\nCard Type: {card_type}")
    print(f"Card #: {card_number}")
    print(f"Name: {name}")
    print(f"Expiration Date: {exp_date}")
    print(f"CVV: {cvv}")
    print("="*40)

if __name__ == "__main__":
    main()