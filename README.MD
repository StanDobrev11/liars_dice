# Liar's Dice
Welcome aboard to the world of Liar's Dice! This pirate-themed dice game is a fun and strategic game of bluffing, 
calling, and guessing. In this version, you can play against upto 5 AI opponents with a choice of regular or wild gameplay.

## Table of Contents
- Rules of the Game
- How to Play
- Game Modes
- Installation and Setup
- License
- Developer Info

## Rules of the Game
Liar’s Dice is a bluffing game played with multiple players, each with a set of dice hidden in their cups. 
The goal is to outbid or call the bluffs of your opponents.

## Objective
The objective of the game is to be the last player with dice remaining. 
Players take turns bidding on how many dice of a certain face they believe are present under all players’ cups. 
Bids can be challenged by calling "Liar!" If the bid is valid, the challenger loses a die. 
If the bid is false, the bidder loses a die.

## Basic Rules
1. Bidding: Players take turns bidding how many dice of a certain face (number) are present under all players’ cups. For example, a bid could be "three 4's", meaning you believe there are at least three dice showing a 4.
2. Increasing the Bid: The next player must either increase the bid or call the previous player a "Liar!" The bid can be increased by either raising the count of the same face or bidding on any particular count of a higher face. For example, if the bid is "three 4's", the next player can either say "four 4's" or "three 5's".
3. Calling "Liar!": If a player thinks the previous bid is false, they can call "Liar!" and all dice are revealed. If the bid is valid (i.e., the number of dice showing the bid face or wild dice is equal or greater), the challenger loses a die. If the bid is false, the bidder loses a die.
4. Wild Dice: In wild mode, all 1's count as wild and can represent any face value.
5. Winning: The game continues until only one player has dice remaining.

## How to Play
### Starting the Game
- Run the game by executing the Game class in your terminal.
```bash
python game.py
```
- The game will prompt you to choose the number of dice (2 to 5 per player) and the number of players (2 to 6, including both human and computer players).
- Choose whether to play the regular version or wild version (wild means that 1's are wild and can be used as any face value).
### Player Turns
- The game alternates turns between human and AI players.
- On your turn, you can either:
  * Place a bid on the number and face of dice you think are present under all cups.
  * Call "Liar!" if you think the previous player’s bid is a bluff.

After each round, the dice are revealed and the game continues based on the result of the challenge.

## Game Modes
### Regular Mode: 
In this mode, all dice faces from 1 to 6 are normal, and players must bid based on exact numbers.
### Wild Mode: 
In this mode, all dice showing a 1 are considered wild and can be used as any face value. This adds an extra layer of strategy and bluffing to the game.

## Installation and Setup
Get the GitRepo and enjoy!
### Requirements
Python 3.x

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute this code. See the LICENSE file for more details.

## Developer Info
Developed by Stan Dobrev.

### Contact Info
- GitHub: https://github.com/StanDobrev11/
- email: dobrev81@gmail.com

## Contribution Guidelines
Feel free to fork this repository and make pull requests to improve the game. Contributions are always welcome, whether it’s for bug fixes, new features, or improvements in gameplay.
