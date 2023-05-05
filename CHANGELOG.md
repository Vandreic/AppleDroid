# **Changelog**
All changes to this project will be documented in this file.

*Date format: [dd-mm-year]*

---

### **Version 0.1**
**Release date:** 29/04-2023
* Created game

---

### **Version 0.2**
**Release date:** 30/04-2023
* Added countdown timer
* Added end-screen

---

### **Version 0.3**
**Release date:** 01/05-2023
* Added start-screen
* Updated code structure

---

### **Version 0.4**

**Release date:** 05/05-2023

* Added gold apple
* Major code and file organization overhaul
  * Replaced single "main.py" with modular files
    * `config.py` Contains game settings, asset paths, and gameplay behavior variables, including player settings
    * `game_logic.py` Manages the main game loop, event handling, and updates game components
    * `game_screen.py` Handles rendering and updating of game screens, displaying game elements, and navigation input
    * `player.py` Represents the player character, handling image loading, positioning, movement, and respawn
    * `apple.py` and `gold_apple.py` Represents the apple(s) collectibles, managing image loading, positioning, and respawn
  * Updated import statements and dependencies accordingly