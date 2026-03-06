# 🏰 Dungeon Quest – Mini Crawler

A compact, fast‑paced dungeon crawler built with **Pygame**, featuring:

- Procedurally generated mazes  
- Smooth tile‑based movement  
- Randomized enemy patrols  
- Collectible coins  
- A goal tile that advances levels  
- Increasing difficulty  
- Score tracking  
- A simple intro screen  

This project is designed to be lightweight, readable, and easy to expand.

---

## 🎮 Gameplay Overview

Each level is a freshly generated maze created using a recursive backtracking algorithm. You begin at the entrance and must navigate to the red **goal tile** while avoiding roaming enemies. Along the way, you can collect coins for extra points.

Reaching the goal:

- Generates a new maze  
- Increases the level counter  
- Adds to your score  

Getting hit by an enemy resets the level without awarding points.

---

## 🧠 Features

- **Procedural Maze Generation**  
  Every level is unique thanks to a recursive carving algorithm.

- **Smooth Movement System**  
  The player slides between tiles rather than teleporting, giving a more polished feel.

- **Enemy AI**  
  Enemies wander randomly but intelligently, choosing valid paths through the maze.

- **Collectibles**  
  Coins spawn in random walkable tiles and reward exploration.

- **Level Progression**  
  Each completed maze increases difficulty and score.

- **Intro Screen**  
  A simple title screen sets the stage before gameplay begins.

---

## ⌨️ Controls

- **W / Up Arrow** – Move up  
- **A / Left Arrow** – Move left  
- **S / Down Arrow** – Move down  
- **D / Right Arrow** – Move right  
- **Enter** – Start the game from the intro screen  

Movement is tile‑based but animated smoothly.

---

## 🛠️ Tech Stack

- **Python 3.x**  
- **Pygame** (2.x recommended)

---

## 🚀 Running the Game

1. Install Pygame:  
   ```bash
   pip install pygame
   ```
2. Run the script:  
   ```bash
   python dungeon_quest.py
   ```

---

## 📦 Project Structure

```
dungeon-quest/
│
├── dungeon_quest.py     # Main game file
├── README.md            # Project documentation
└── assets/              # (Optional) future sprites, sounds, etc.
```

---

## 🌱 Future Ideas

- Player health and combat  
- Multiple enemy types  
- Power‑ups (speed boost, shield, invisibility)  
- Sound effects and music  
- Custom sprites instead of rectangles  
- A proper menu system  
- A roadmap section for future features  

Would you like the README to include screenshots or ASCII diagrams of the maze layout?
