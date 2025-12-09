#!/usr/bin/env python3
# Name: Steven Gerard Bogus III
# Date: 12/10/2023 (Original script) - Updated: 12/07/2025
# Final Project: To write a video poker sim game in Python using tkinter
# Assumptions: Card images are stored in a subdirectory named 'library'.

import tkinter as tk
from tkinter import simpledialog, messagebox
from random import shuffle
import os

class VideoPoker:
    def __init__(self, player_name):
        self.root = tk.Tk()
        self.root.title("Jacks or Better Video Poker")
        self.player_name = player_name
        self.bank_file = f"{self.player_name}.bank"
        self.deck_size = 52
        self.bet = 0
        self.bank = 0
        self.game_phase = "bet"  # states: "bet", "deal", "draw"
        self.current_hand = []
        self.held_cards = [False] * 5
        self.card_labels = []
        self.discard_buttons = []

        self.load_bank()
        self.load_images()
        self.create_gui()

    def load_bank(self):
        try:
            with open(self.bank_file, "r") as file:
                # use .strip() to remove any leading/trailing whitespace/newlines
                self.bank = int(file.read().strip()) 
        except (FileNotFoundError, ValueError):
            self.bank = 1000  # initial bank value if file is missing or invalid
            self.save_bank()

    def save_bank(self):
        with open(self.bank_file, "w") as file:
            file.write(str(self.bank))

    def load_images(self):
        self.card_images = {}
        self.image_folder = "library"
        
        if not os.path.isdir(self.image_folder):
            messagebox.showerror("Image Error", f"The '{self.image_folder}' folder was not found. Please ensure it is in the same directory as Final.py.")
            return

        # load all .gif files from 'library' folder
        for filename in os.listdir(self.image_folder):
            if filename.endswith(".gif"):
                card_name = filename.split(".")[0]
                try:
                    full_path = os.path.join(self.image_folder, filename)
                    self.card_images[card_name] = tk.PhotoImage(file=full_path)
                except Exception as e:
                    print(f"Error loading image {filename}: {e}")

        if not self.card_images:
            print("Error: No card images found.")
            messagebox.showerror("Image Error", "No card images loaded. Check file paths and formats.")
        elif "Yellow_back" not in self.card_images:
             print("Warning: 'Yellow_back.gif' not loaded.")
        else:
             print(f"Successfully loaded {len(self.card_images)} card images.")


    def create_deck(self):
        # creates full 52-card deck based on expected file names
        ranks = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.full_deck = [f"{rank}_of_{suit}" for rank in ranks for suit in suits]
        shuffle(self.full_deck)
        self.deck_in_play = self.full_deck[:]

    def toggle_hold(self, card_index):
        if self.game_phase == "deal":
            self.held_cards[card_index] = not self.held_cards[card_index]
            # updates the button text to reflect the hold status
            hold_status = "**HELD**" if self.held_cards[card_index] else "DISCARD"
            self.discard_buttons[card_index].config(text=hold_status, relief=tk.RAISED if self.held_cards[card_index] else tk.FLAT)

    def bet_one_coin(self):
        if self.game_phase == "bet" and self.bank >= 1 and self.bet < 5: 
            self.bet += 1
            self.bank -= 1
            self.update_bet_label()
            self.deal_button.config(state=tk.NORMAL)

    def bet_max(self):
        if self.game_phase == "bet":
            bet_increase = min(5 - self.bet, self.bank) 
            self.bet += bet_increase
            self.bank -= bet_increase
            self.update_bet_label()
            self.deal_button.config(state=tk.NORMAL)

    def start_deal(self):
        if self.game_phase == "bet" and self.bet > 0:
            self.game_phase = "deal"
            self.create_deck()
            self.deal_initial_hand()
            self.deal_button.config(text="DRAW", command=self.finish_draw)
            self.bet_one_button.config(state=tk.DISABLED)
            self.bet_max_button.config(state=tk.DISABLED)
            
            # enable hold buttons
            for btn in self.discard_buttons:
                btn.config(state=tk.NORMAL, text="DISCARD")
                
        elif self.game_phase == "bet" and self.bet == 0:
            messagebox.showwarning("Bet Required", "Please place a bet before dealing.")


    def deal_initial_hand(self):
        # reset hold status and button appearance
        self.held_cards = [False] * 5
        for i, btn in enumerate(self.discard_buttons):
            btn.config(text="DISCARD", relief=tk.FLAT)
            
        # draw 5 new cards
        self.current_hand = [self.deck_in_play.pop() for _ in range(5)]
        self.display_hand()

    def finish_draw(self):
        if self.game_phase == "deal":
            self.game_phase = "draw"
            
            # draw replacements for non-held cards
            for i, held in enumerate(self.held_cards):
                if not held:
                    new_card = self.deck_in_play.pop()
                    self.current_hand[i] = new_card
                
            # disable hold buttons and update display
            for btn in self.discard_buttons:
                btn.config(state=tk.DISABLED, text="") 
                
            self.display_hand()
            
            # calculate score and process winnings
            score = self.calculate_score(self.current_hand)
            self.process_winnings(score)
            
            # prepare for the next round
            self.game_phase = "bet"
            self.bet = 0 
            self.update_bet_label()
            self.deal_button.config(text="DEAL", command=self.start_deal, state=tk.DISABLED)
            self.bet_one_button.config(state=tk.NORMAL)
            self.bet_max_button.config(state=tk.NORMAL)


    def calculate_score(self, hand):
        # rank values for scoring
        rank_map = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, 
                    "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 11, "Queen": 12, "King": 13, "Ace": 14}
        
        ranks = []
        suits = []
        for card_name in hand:
            try:
                rank, suit = card_name.split("_of_")
                ranks.append(rank)
                suits.append(suit)
            except ValueError:
                print(f"Error parsing card name: {card_name}")
                return 0 

        if len(ranks) != 5: return 0

        # get sorted numerical rank values
        try:
            rank_values = sorted([rank_map[rank] for rank in ranks])
        except KeyError:
            print("Error: Unrecognized card rank.")
            return 0
            
        rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
        suit_counts = {suit: suits.count(suit) for suit in set(suits)}

        is_flush = 5 in suit_counts.values()
        is_straight = self._is_straight_by_value(rank_values)

        # 1. royal flush (10, J, Q, K, A, same suit)
        if is_flush and rank_values == [10, 11, 12, 13, 14]:
            return 2000

        # 2. straight flush
        if is_straight and is_flush:
            return 250

        # 3. four of a kind
        if 4 in rank_counts.values():
            return 125

        # 4. full house
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            return 40

        # 5. flush
        if is_flush:
            return 25

        # 6. straight
        if is_straight:
            return 20

        # 7. three of a kind
        if 3 in rank_counts.values():
            return 15

        # 8. two pair
        if list(rank_counts.values()).count(2) == 2:
            return 10

        # 9. jacks or better (pair of J, Q, K, or A)
        high_pairs = [11, 12, 13, 14] 
        if any(rank_map[rank] in high_pairs and count == 2 for rank, count in rank_counts.items()):
            return 5

        return 0  # no win

    def _is_straight_by_value(self, rank_values):
        # rank_values must be sorted: [2, 3, 4, 5, 14] for A-5 straight
        is_regular_straight = all(rank_values[i] == rank_values[0] + i for i in range(5))
        is_low_ace_straight = rank_values == [2, 3, 4, 5, 14] # A-2-3-4-5
        return is_regular_straight or is_low_ace_straight

    def process_winnings(self, score):
        winnings = score * self.bet
        if winnings > 0:
            self.bank += winnings
            self.save_bank()
            messagebox.showinfo("Winner!", f"You won {winnings} coins with a {self.get_hand_name(score)}!")
        else:
            messagebox.showinfo("No Win", "Sorry, better luck next time!")
        
        self.bet = 0
        self.update_bet_label()

    def get_hand_name(self, score):
        if score == 2000: return "Royal Flush"
        if score == 250: return "Straight Flush"
        if score == 125: return "Four of a Kind"
        if score == 40: return "Full House"
        if score == 25: return "Flush"
        if score == 20: return "Straight"
        if score == 15: return "Three of a Kind"
        if score == 10: return "Two Pair"
        if score == 5: return "Jacks or Better"
        return "Nothing"

    def display_hand(self):
        # clear existing card display
        for label in self.card_labels:
            label.destroy()
        self.card_labels = []

        # display the current hand
        for i, card in enumerate(self.current_hand):
            card_image = self.card_images.get(card)
            
            if card_image is None:
                # fallback if image is missing (e.g., an unprovided card like 7_of_Spades)
                card_image = self.card_images.get("Yellow_back") 
                if card_image is None:
                    label = tk.Label(self.root, text=f"{card}", borderwidth=2, relief="solid", width=10, height=5)
                else:
                    label = tk.Label(self.root, image=card_image)
            else:
                label = tk.Label(self.root, image=card_image)
            
            label.grid(row=2, column=i, padx=5, pady=5)
            self.card_labels.append(label)

    def display_initial_board(self):
        # display the card backs before the first deal
        for i in range(5):
            back_image = self.card_images.get("Yellow_back")
            if back_image:
                 label = tk.Label(self.root, image=back_image)
            else:
                 label = tk.Label(self.root, text="Card Back", borderwidth=2, relief="solid", width=10, height=5)
                 
            label.grid(row=2, column=i, padx=5, pady=5)
            self.card_labels.append(label)


    def update_bet_label(self):
        self.bet_label.config(text=f"Player: {self.player_name}\nBank: ${self.bank}\n"
                                   f"Bet: ${self.bet}/5 Coins")

    def create_gui(self):
        # --- control/info area (Row 0, 1) ---
        self.bet_label = tk.Label(self.root, text="", justify=tk.LEFT)
        self.bet_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)
        self.update_bet_label() 

        paytable_button = tk.Button(self.root, text="View Paytable", command=self.show_paytable)
        paytable_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.bet_one_button = tk.Button(self.root, text="Bet One Coin", command=self.bet_one_coin)
        self.bet_one_button.grid(row=1, column=0, padx=5, pady=5)

        self.bet_max_button = tk.Button(self.root, text="Bet Max", command=self.bet_max)
        self.bet_max_button.grid(row=1, column=1, padx=5, pady=5)

        self.deal_button = tk.Button(self.root, text="DEAL", command=self.start_deal, state=tk.DISABLED)
        self.deal_button.grid(row=1, column=2, padx=5, pady=5)
        
        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        exit_button.grid(row=1, column=4, padx=5, pady=5)
        
        # --- card display area (Row 2) ---
        self.display_initial_board()
        
        # --- hold buttons area (Row 3) ---
        self.discard_buttons = []
        for i in range(5):
            btn = tk.Button(self.root, text="", command=lambda i=i: self.toggle_hold(i), state=tk.DISABLED, width=10)
            btn.grid(row=3, column=i, padx=5, pady=5)
            self.discard_buttons.append(btn)

        self.root.mainloop()
        
    def show_paytable(self):
        paytable_text = (
            "💰 Jacks or Better Paytable 💰\n"
            "----------------------------\n"
            "Royal Flush:      2000 (Payout based on 1 coin bet)\n"
            "Straight Flush:   250\n"
            "4 of a Kind:      125\n"
            "Full House:       40\n"
            "Flush:            25\n"
            "Straight:         20\n"
            "3 of a Kind:      15\n"
            "Two Pair:         10\n"
            "Jacks or Better:  5"
        )
        messagebox.showinfo("Paytable", paytable_text)


if __name__ == "__main__":
    player_name = simpledialog.askstring("Player Name", "Enter your name:")
    if player_name:
        poker_game = VideoPoker(player_name)
    else:
        print("Game closed. No player name entered.")