Rock Paper Scissors (Tkinter)
=============================

Simple GUI for Rock–Paper–Scissors implemented in Python with Tkinter.

Files
- `rock_paper_scissors.py`: The main module; contains game logic and the `RPSApp` Tkinter application.
- `README_RPS.md`: This file (usage and API reference).

Run
From PowerShell (Windows):

```powershell
python c:\Codigos\rock_paper_scissors.py
```

This opens a small window with three buttons: Rock, Paper, Scissors. Click a button to play one round against the computer. The UI shows both choices, the round result, and running scores. Use Reset to zero scores or Quit to close the window.

API (for importing)
- `get_computer_choice()` -> str
  - Returns a random move: `'rock'`, `'paper'`, or `'scissors'`.

- `determine_winner(player, computer)` -> str
  - Determine the winner of a single round.
  - Parameters: `player` and `computer` must be one of `'rock'`, `'paper'`, `'scissors'`.
  - Returns: `'player'`, `'computer'`, or `'tie'`.
  - Raises `ValueError` if either argument is not a valid move.

Notes
- Importing the module does not open the GUI (the GUI is only launched when `__name__ == '__main__'`).
- The game logic functions are documented and validated so you can import them into unit tests or other programs.

Possible enhancements
- Add a "best of N" match mode.
- Add keyboard shortcuts and accessibility labels.
- Package as an executable with PyInstaller for distribution.
