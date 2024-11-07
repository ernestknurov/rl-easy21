import numpy as np

class Environment:
    def __init__(self, logger) -> None:
        self.logger = logger
        self.deck = np.arange(1, 11) # A deck of cards from 1 to 10
        self.color_prob = {'red': 1/3, 'black': 2/3} # 0th index - red, 1th index - black
        self.color_to_sign = {'red': -1, 'black': 1} # red - subtract, black - add
        self.nA = 2 # action space dimension
        self.nS = 2 # state space dimension
    
    def draw(self):
        """Draw card from the deck. Return num and color of the card."""
        card_value = np.random.choice(self.deck, replace=True) # we're sampling with replacing
        card_color = np.random.choice(list(self.color_prob.keys()), p=list(self.color_prob.values()))
        return int(card_value), card_color

    def reset(self):
        "Reset the environment and return initial state"
        # state is tuple of dealer first card and player sum
        dealer_sum = np.random.choice(self.deck) # Dealer starts with a black card
        player_sum = np.random.choice(self.deck) # Player starts with a black card
        return int(dealer_sum), int(player_sum)
    
    def is_terminal(self, cards_sum):
        return cards_sum > 21 or cards_sum < 1
    
    def dealer_step(self,  dealer_sum):
        """Return final dealer sum and if he's gone bust."""
        # dealer hits cards while the sum < 17 or he goes bust
        while dealer_sum < 17: 
            card_value, card_color = self.draw()
            self.logger.info(f"Dealer card: {card_value} {card_color}")
            dealer_sum += card_value * self.color_to_sign[card_color]
            if self.is_terminal(dealer_sum):
                return dealer_sum, True  # Dealer busts
        return dealer_sum, False
    
    def step(self, current_state: list, action: int):
        """Make one step in Easy21 game. Return next state, reward and boolean flag is the state is terminal."""
        dealer_sum, player_sum = current_state

        # Check if we're already in terminal state
        if self.is_terminal(player_sum):
            return current_state, 0, True
        
        if action == 0: # hit
            card_value, card_color = self.draw()
            self.logger.info(f"Player card: {card_value} {card_color}")
            player_sum += card_value * self.color_to_sign[card_color]
            if self.is_terminal(player_sum):
                reward = -1 # game lose
                return (dealer_sum, player_sum), reward, True  # Terminal state
            else:
                reward = 0 # continue the game

        if action == 1: # stick
            # If user stick, then dealer starts to take cards
            dealer_sum, dealer_bust = self.dealer_step(dealer_sum)
            # Calculate the reward 
            if dealer_bust or player_sum > dealer_sum:
                reward = 1 # win
            elif player_sum == dealer_sum:
                reward = 0 # draw
            else:
                reward = -1 # lose

        next_state = dealer_sum, player_sum
        is_terminal_state = (action == 1 or self.is_terminal(player_sum))
        return next_state, reward, is_terminal_state