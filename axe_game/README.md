# Wood Collector 2D Game

A simple 2D game where you collect wood and sell it at the market to earn gold.

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. Controls:
- Arrow keys: Move the player
- SPACE: Collect wood (when near trees and have an axe)
- B: Buy axe (when at market and have enough gold)
- S: Sell wood (when at market and have wood)

3. Game Elements:
- Brown square: Player
- Green squares: Trees
- Gold square: Market
- White background: Game world

4. Game Rules:
- You start with 50 gold
- An axe costs 50 gold
- Each tree hit gives you 15 wood
- Each wood unit sells for 1.67 gold
- Axe health decreases with each use
- You need an axe to collect wood

## Goal
Collect wood from trees and sell it at the market to earn as much gold as possible! 