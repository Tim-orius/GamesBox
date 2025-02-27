# Timorius' GamesBox

This repository contains some fun coding adventures into some random games. 
There is no real order or sense to the games.

## Zwanzigachtundvierzig

This game is a (for the most part) self-made version of the game 2048 (some 
parts were edited with ChatGPT due to me being lazy). It is made with a 
tkinter UI and features an AI Agent (using a greedy search algorithm).

### Controls:

- Keyboard arrow UP: move up
- Keyboard arrow DOWN: move down
- Keyboard arrow LEFT: move left
- Keyboard arrow RIGHT: move right
- Keyboard ENTER: toggle auto play
- Keyboard ESCAPE: restart / refresh

The instructions can also be read in the options menu -> help

## Minesweeper

A classic. [Further Info](https://en.wikipedia.org/wiki/Minesweeper_(video_game))

### Know ~~bugs~~ features

- Sometimes less mines than set are spawned or some removed during the setup 
  of the hint numbers
- The scoreboard disappears after performing any click for unknown reasons
- When images are used for display, images remain on a tile when displayed 
  once. So far there is no logic in place to remove images from a tile (e.g. 
  flag image when removing the flag or after a flagged tile is revealed is 
  still present).

## Sudoku

Sudoku contains a sudoku-board-*creator*. It creates a random normal sudoku 
board and the solution.

**Note**: Currently does not use a solver to check for resolvability or 
unique solutions.
