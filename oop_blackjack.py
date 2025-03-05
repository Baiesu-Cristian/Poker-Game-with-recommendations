import random
from recommendation import *

class Deck:
    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['♡', '♢', '♤', '♧']
    DECK_COUNT = 6

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)
    
    def create_deck(self):
        self.cards = [Card(value, suit) for value in self.VALUES for suit in self.SUITS] * self.DECK_COUNT
        random.shuffle(self.cards)


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value}{self.suit}"
    
    def __repr__(self):
        return str(self)
    
    @property
    def card_value(self):
        if self.value in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            return int(self.value)
        elif self.value in ['J', 'Q', 'K']:
            return 10
        else:
            return 11
        

class Player:
    def __init__(self):
        self.hand = []
        self.aces_counted_as_1 = 0

    def __len__(self):
        return len(self.hand)
    
    def is_busted(self):
        return self.hand_value > 21
    
    def reset(self):
        self.hand = []
        self.aces_counted_as_1 = 0
    
    @property
    def hand_value(self):
        value = sum(card.card_value for card in self.hand)
        self.aces_counted_as_1 = 0
        while value > 21 and self.ace_count > 0:
            value -= 10
            self.aces_counted_as_1 += 1
        return value
    
    @property
    def ace_count(self):
        return len([card for card in self.hand if card.value == 'A']) - self.aces_counted_as_1
    

class Human(Player):
    def __init__(self, chips):
        super().__init__()
        self.chips = chips

    def make_bet(self):
        print(f"You have {self.chips} chips")
        while True:
            try:
                bet = int(input("Make a bet: "))
                if bet <= 0:
                    print("Bet must be greater than zero.")
                elif bet > self.chips:
                    print("You don't have enough chips")
                else:
                    self.chips -= bet
                    return bet
            except ValueError:
                print("Invalid number, please enter a valid integer.")
            

class Dealer(Player):
    def __init__(self):
        super().__init__()


class Game:
    RESHUFFLE_THRESHOLD = 0.25 * Deck.DECK_COUNT

    def __init__(self):
        self.deck = Deck()
        self.player = Human(100)
        self.dealer = Dealer()
        self.bet = 0
        self.choice = ""

    def first_hand(self):
        for _ in range(2):
            self.add_card(self.player)
            self.add_card(self.dealer)

    def show_hands(self, show = False):
        print(f"Your cards: {self.player.hand}")
        print(f"{self.player.hand_value} points")
        print()
        if not show:
            print(f"Dealer's hand: [{self.dealer.hand[0]}, ()]")
            print(f"{self.dealer.hand[0].card_value} points")
        else:
            print(f"Dealer's cards: {self.dealer.hand}")
            print(f"{self.dealer.hand_value} points")
        print("-" * 30)

    def can_split(self):
        return len(self.player) == 2 and self.player.hand[0].value == self.player.hand[1].value
    
    def blackjack(self):
        if self.player.hand_value == 21 or self.dealer.hand_value == 21:
            self.show_hands(True)
            if self.player.hand_value == 21 and self.dealer.hand_value != 21:
                print("You have a blackjack!")
                self.player.chips += round(2.5 * self.bet)
            elif self.player.hand_value == 21 and self.dealer.hand_value == 21:
                print("You both have a blackjack!")
                self.player.chips += self.bet
            elif self.player.hand_value != 21 and self.dealer.hand_value == 21:
                print("The dealer has a blackjack!")
            print()
            return True
        else:
            return False
        
    def recommend(self, player, dealer):
        if self.choice == "sp":
            return simple_rec(self.player.hand_value, self.dealer.hand[0].card_value)
        if self.can_split():
            recom = split_rec(player // 2, dealer)
        elif self.player.ace_count > 0:
            recom = aces_rec(player - 11, dealer)
        else:
            recom = simple_rec(self.player.hand_value, self.dealer.hand[0].card_value)
        if recom == "double" and (len(self.player) > 2 or self.player.chips < self.bet):
            recom = "hit"
        return recom

    def question(self):
        print("Recommendation:", self.recommend(self.player.hand_value, self.dealer.hand[0].card_value))
        if len(self.player) == 2 and self.can_split() and self.player.chips >= self.bet:
            return input("Hit, stand, double or split? [h/s/d/sp] ")
        elif len(self.player) == 2 and self.player.chips >= self.bet:
            return input("Hit, stand or double? [h/s/d] ")
        else:
            return input("Hit or stand? [h/s] ")
        
    def reset_game(self):
        self.player.reset()
        self.dealer.reset()
        self.bet = 0
    
    def add_card(self, person):
        card = self.deck.cards.pop()
        person.hand.append(card)
    
    def hit(self, person):
        self.add_card(person)
        if person.is_busted():
            self.show_hands(True)
            print("You busted!\n")
        else:
            self.show_hands()

    def winner(self):
        if self.dealer.is_busted():
            print("Dealer busted. You win!\n")
            self.player.chips += 2 * self.bet
        elif self.player.hand_value > self.dealer.hand_value:
            print("You win!\n")
            self.player.chips += 2 * self.bet
        elif self.player.hand_value == self.dealer.hand_value:
            print("Draw!\n")
            self.player.chips += self.bet
        else:
            print("You lost!\n")

    def stand(self):
        self.show_hands(True)
        while self.dealer.hand_value < 17:
            self.add_card(self.dealer)
            self.show_hands(True)
        self.winner()

    def double(self):
        self.player.chips -= self.bet
        self.bet *= 2
        self.hit(self.player)
        if not self.player.is_busted():
            self.stand()

    def split_stand(self):
        self.show_split(True)
        while self.dealer.hand_value < 17:
            self.add_card(self.dealer)
            self.show_split(True)
        self.split_winner()

    def split_winner(self):
        case1 = self.hand1.hand_value == self.dealer.hand_value
        case2 = self.hand1.hand_value > self.dealer.hand_value and not self.hand1.is_busted()
        case3 = self.hand1.hand_value < self.dealer.hand_value or self.hand1.is_busted()
        case4 = self.hand2.hand_value == self.dealer.hand_value
        case5 = self.hand2.hand_value > self.dealer.hand_value and not self.hand2.is_busted()
        case6 = self.hand2.hand_value < self.dealer.hand_value or self.hand2.is_busted()
        case7 = self.hand1.is_busted()
        case8 = self.hand2.is_busted()
        case9 = self.dealer.is_busted()
        if (case2 and case5) or (case9 and not case7 and not case8):
            print("You won both hands!\n")
            self.player.chips += 4 * self.bet
        elif (case1 and case5) or (case2 and case4):
            print("You won a hand, drew the other!\n")
            self.player.chips += 3 * self.bet
        elif (case2 and case6) or (case3 and case5) or (case9 and (case7 or case8)):
            print("You won a hand, lost the other!\n")
            self.player.chips += 2 * self.bet
        elif (case1 and case6) or (case3 and case4) or (case7 and case4) or (case8 and case1):
            print("You lost a hand, drew the other!\n")
            self.player.chips += self.bet
        elif (case3 and case6):
            print("You lost both hands!\n")
        else:
            print("You drew both hands!\n")
            self.player.chips += 2 * self.bet

    def show_split(self, show=False):
        if not show:
            if self.curr_hand.hand == self.hand1.hand:
                print(f"Your first hand: {self.curr_hand.hand}")
            else:
                print(f"Your second hand: {self.curr_hand.hand}")
            print(f"{self.curr_hand.hand_value} points\n")
            print(f"Dealer's hand: [{self.dealer.hand[0]}, ()]")
            print(f"{self.dealer.hand[0].card_value} points")
        else:
            print(f"Your first hand: {self.hand1.hand}")
            print(f"{self.hand1.hand_value} points\n")
            print(f"Your second hand: {self.hand2.hand}")
            print(f"{self.hand2.hand_value} points\n")
            print(f"Dealer's cards: {self.dealer.hand}")
            print(f"{self.dealer.hand_value} points")
        print("-" * 30)

    def split(self):
        self.player.chips -= self.bet
        self.hand1 = Player()
        self.hand2 = Player()
        self.hand1.hand.append(self.player.hand[0])
        self.hand2.hand.append(self.player.hand[1])
        self.add_card(self.hand1)
        self.add_card(self.hand2)
        if self.player.hand[0].value == 'A':
            self.split_stand()
            return
        self.curr_hand = self.hand1
        self.show_split()
        while True:
            print("Recommendation:", self.recommend(self.curr_hand.hand_value, self.dealer.hand[0].card_value))
            choice = input("Hit or stand? [h/s] ")
            print()
            if choice == 'h':
                self.add_card(self.curr_hand)
                self.show_split()
                if self.curr_hand.is_busted():
                    print("You busted that hand!\n")
                    if self.curr_hand.hand == self.hand1.hand:
                        self.curr_hand = self.hand2
                        self.show_split()
                    else:
                        if self.hand1.is_busted() and self.hand2.is_busted():
                            self.show_split(True)
                            print("You busted both hands!\n")
                        else:
                            self.split_stand()
                        break
            elif choice == 's':
                if self.curr_hand.hand == self.hand1.hand:
                    self.curr_hand = self.hand2
                    self.show_split()
                else:
                    self.split_stand()
                    break
            else:
                print("Invalid choice")

    def player_turn(self):
        while True:
            self.choice = self.question()
            print()
            if self.choice == 'h':
                self.hit(self.player)
                if self.player.is_busted():
                    break
            elif self.choice == 's':
                self.stand()
                break
            elif self.choice == 'd' and len(self.player.hand) == 2 and self.player.chips >= self.bet:
                self.double()
                break
            elif self.choice == 'sp' and self.can_split() and self.player.chips >= self.bet:
                self.split()
                break
            else:
                print("Invalid choice\n")

    def play(self):
        self.deck.create_deck()
        while True:
            if self.player.chips == 0:
                print("You lost all your chips")
                break
            self.bet = self.player.make_bet()
            if self.bet == 0:
                break
            print("-" * 30)
            if len(self.deck) < self.RESHUFFLE_THRESHOLD:
                print("Reshuffling the cards\n")
                self.deck.create_deck()
            self.first_hand()
            if self.blackjack():
                self.reset_game()
                continue
            self.show_hands()
            self.player_turn()
            self.reset_game()

def main():
    game = Game()
    game.play()

if __name__ == '__main__':
    main()
