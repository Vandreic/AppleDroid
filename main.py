"""
AppleDroid v0.6

A small python game where you control an Android with the objective of collecting as many apples as possible.


TO-DO:
- BUG:
    - Fix apple spawn so they do not spawn inside each other
    - Fix gold apple spawn check: Gold apple keeps spawning after game ends 
      - Results in gold apple sometimes already being spawned after game restart
      - Spawn timer aLso needs to reset after player collision
- Add background music
    - Problems loading music files using 'pygame.mixer.music'... I've tried: .wav, .ogg, .mp3, but none worked
- Improve readibility of highscore and countdown timer texts
- Improve readibility of code
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
