# Poker Game

### Overview

This project is a console-based implementation of the classic card game Blackjack, also known as 21. The game is designed to simulate a real-life casino experience, allowing players to bet chips, make strategic decisions, and play against a dealer. The game is implemented in Python using object-oriented programming principles, making it modular and easy to extend.

### Features

- **Multiple Decks**: The game uses six decks of cards, which is a common practice in casinos to prevent card counting.
- **Player and Dealer**: The game features a human player and a dealer, each with their own hand of cards.
- **Betting System**: Players start with a set amount of chips and can place bets before each round. The game includes logic for handling bets, including doubling down and splitting.
- **Card Recommendations**: The game provides recommendations for the player based on basic Blackjack strategy, helping them make informed decisions.
- **Splitting and Doubling**: Players can choose to split their hand if they have two cards of the same value or double their bet under certain conditions.
- **Automatic Reshuffling**: The deck is reshuffled when a certain percentage of the cards have been dealt, simulating a real casino environment.

### Game Rules

1. **Objective**: The goal of Blackjack is to have a hand value closer to 21 than the dealer's hand without exceeding 21.
2. **Card Values**: Number cards are worth their face value, face cards (J, Q, K) are worth 10, and Aces can be worth 1 or 11, depending on which value is more favorable for the hand.
3. **Gameplay**:
   - The player places a bet.
   - Both the player and the dealer are dealt two cards. The player's cards are face up, while the dealer has one card face up and one face down.
   - The player can choose to "hit" (take another card) or "stand" (end their turn).
   - The player can also choose to "double" (double their bet and take one more card) or "split" (if they have two cards of the same value, they can split them into two separate hands).
   - The dealer must hit until their hand value is at least 17.
   - The winner is determined by whose hand is closer to 21 without exceeding it.

### Code Structure

- **Deck Class**: Manages the creation and shuffling of the deck(s) of cards.
- **Card Class**: Represents a single card with a value and suit.
- **Player Class**: Represents a player in the game, including their hand and actions.
- **Human Class**: Inherits from Player and includes additional functionality for betting.
- **Dealer Class**: Inherits from Player and includes dealer-specific behavior.
- **Game Class**: Manages the overall game flow, including dealing cards, handling player actions, and determining the winner.

### Installation and Usage

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/yourusername/blackjack-game.git
   cd blackjack-game
   ```

2. **Install Dependencies**: 
   Ensure you have Python installed on your system. This project does not have external dependencies beyond the standard library.

3. **Run the Game**: 
   Execute the game by running the following command:
   ```bash
   python oop_blackjack.py
   ```

4. **Gameplay**: 
   Follow the on-screen instructions to place bets and make decisions. The game will provide recommendations based on basic strategy.
