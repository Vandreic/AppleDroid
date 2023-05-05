"""
AppleDroid v0.4

A small python game where you control an Android with the objective of collecting as many apples as possible.


TO-DO:
- BUG: Fix apple spawn
       * No spawn inside highscore & countdown text
       * No spawn inside player spawn area

- Change "SPACE" key input to pygame keys event instead?
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
