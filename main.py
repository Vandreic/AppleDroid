"""
AppleDroid v0.4

A small python game where you control an Android with the objective of collecting as many apples as possible.


TO-DO:
- Add spawn restrictions to gold apple (Combine files into one?)
- Fix highscore for end-screen
"""


# Import modules
from game_components.core.game_logic import Game

# Main function
def main():
    game = Game() # Create game
    
    while True: # Needed in order to run game constantly
        game.update() # Run game loop

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
