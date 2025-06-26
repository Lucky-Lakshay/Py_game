# 🚀 Space Shooter[::-1]

A fast-paced 2D space shooting game built with **Pygame**. Dodge meteors, shoot lasers, and survive as long as you can!

---

## 🎮 How to Play

- Move your spaceship using **arrow keys**.
- Press **Spacebar** to shoot lasers and destroy meteors.
- Survive as long as possible to increase your score.
- If a meteor hits you, you lose a life.
- You have **3 lives** — once all are lost, the game is over.

---

## 🎮 Controls

| Key         | Action                 |
|-------------|------------------------|
| ← / →       | Move left / right      |
| ↑ / ↓       | Move up / down         |
| Spacebar    | Fire laser (cooldown)  |
| R           | Restart after Game Over |
| Q           | Quit after Game Over   |

---

## 🛠 Features & Changes Implemented

### ✅ Gameplay Mechanics
- Laser cooldown system (no spamming).
- Animated meteor rotation and movement.
- Collision detection for player-meteor and laser-meteor.

### ✅ UI & UX
- Score system based on survival time.
- Lives system with 3 lives total.
- Restart screen after death:
  - Displays **Game Over** message.
  - Shows **final score**.
  - Option to **Restart (R)** or **Quit (Q)**.
  
### ✅ Visual Polish
- Stars now **animate downward** to simulate space movement.
- Smooth **delta time-based movement** for consistent speed on all systems.

---

## 📦 Requirements

- Python 3.7+
- Pygame

Install pygame via pip if not already:

```bash
pip install pygame-ce
