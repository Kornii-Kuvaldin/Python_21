import random


class Game21:
    def __init__(self):
        # Score statistics
        self.playerWins = 0
        self.dealerWins = 0
        # Start immediately with a fresh round
        self.new_round()

    # ROUND MANAGEMENT

    def new_round(self):
        """
        Prepares for a new round
        Suggested process:
        - Create and shuffle a new deck
        - Reset card pointer
        - Empty both hands
        - Reset whether the dealer's hidden card has been revealed
        """
        self.deck = self.create_deck()
        random.shuffle(self.deck)

        # Instead of removing cards from the deck,
        # we keep an index of the "next card" to deal.
        self.deck_position = 0

        # Hands start empty; cards will be dealt after UI calls deal_initial_cards()
        self.player_hand = []
        self.dealer_hand = []

        # The first dealer card starts hidden until Stand is pressed
        self.dealer_hidden_revealed = False

    def deal_initial_cards(self):
        """
        Deal two cards each to player and dealer.
        """
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]

    # DECK AND CARD DRAWING

    def create_deck(self):
        """
        Create a standard 52-card deck represented as text strings, e.g.:
        'A♠', '10♥', 'K♦'.

        Ranks: A, 2–10, J, Q, K
        Suits: spades, hearts, diamonds, clubs (with unicode symbols)
        """
        ranks = ["A"] + [str(n) for n in range(2, 11)] + ["J", "Q", "K"]
        suits = ["♠", "♥", "♦", "♣"]
        return [f"{rank}{suit}" for rank in ranks for suit in suits]

    def draw_card(self):
        card = self.deck[self.deck_position]
        self.deck_position += 1
        return card

    # HAND VALUES + ACE HANDLING

    def card_value(self, card):
        rank = card[:-1]  # everything except the suit symbol

        if rank in ["J", "Q", "K"]:
            return 10

        if rank == "A":
            return 11  # Initially treat Ace as 11

        # Otherwise it's a number from 2 to 10
        return int(rank)

    def hand_total(self, hand):
        total = sum(self.card_value(card) for card in hand)  # Adds all cards in a given hand
        # Ace count
        ace_count = sum(1 for card in hand if "A" in card)  # changed from rank check to not crash
        # Bust handling
        # We will check if our current total with aces as 11 will bust as, and if they will, treat them as 1 while subtracting them from ace_count so they don't doubly add
        while ace_count > 0 and total > 21:
            total -= 10
            ace_count -= 1
        return total

    # PLAYER ACTIONS

    # Draws a card from a deck and adds it to the player's hand
    def player_hit(self):
        card = self.draw_card()
        self.player_hand.append(card)
        return card

    # Returns total value of player's hand
    def player_total(self):
        return self.hand_total(self.player_hand)

    # DEALER ACTIONS

    # Set dealer's hidden status to True which will show the hand to player
    def reveal_dealer_card(self):
        self.dealer_hidden_revealed = True

    # Returns dealer total hand value
    def dealer_total(self):
        return self.hand_total(self.dealer_hand)

    # Does the dealer's action. After the player passes, dealers draws until they hit at least 17
    def play_dealer_turn(self):
        while self.dealer_total() < 17:
            self.dealer_hand.append(self.draw_card())

    # WINNER DETERMINATION

    def decide_winner(self):
        playerTotal = self.player_total()
        dealerTotal = self.dealer_total()
        # First check for busts, then check for who has a higher total
        if playerTotal > 21:
            self.dealerWins+=1
            return "Player bust!"
        if dealerTotal > 21:
            self.playerWins+=1
            return "Dealer bust!"
        if playerTotal > dealerTotal:
            self.playerWins+=1
            return "Player won!"
        elif dealerTotal > playerTotal:
            self.dealerWins+=1
            return "Dealer won!"
        elif dealerTotal == playerTotal:
            return "Draw!"
