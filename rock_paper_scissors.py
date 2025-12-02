"""Simple Rock-Paper-Scissors GUI using Tkinter.

This module provides both game logic functions and a Tkinter GUI for
playing Rock-Paper-Scissors against a computer opponent. It tracks
scores (wins, losses, ties) and maintains a detailed round-by-round
history.

Quick Start
-----------
    python rock_paper_scissors.py

The GUI displays three buttons (Rock, Paper, Scissors), a result label,
detailed scoreboard (player wins, computer wins, ties), and a scrollable
round history. Use Reset to clear scores or Quit to exit.

Module API
----------
For importing into other programs:
    - `get_computer_choice() -> str`
        Returns a random move: 'rock', 'paper', or 'scissors'.
    - `determine_winner(player: str, computer: str) -> str`
        Determines the round winner. Raises ValueError if inputs are invalid.

Design Notes
------------
Game logic is intentionally separate from the GUI (RPSApp class) so the
logic can be imported and tested independently. The GUI only launches
when __name__ == '__main__', making safe imports possible.
"""

import random
import tkinter as tk
from typing import Literal


def get_computer_choice() -> Literal['rock', 'paper', 'scissors']:
    """Return a random move for the computer.

    Returns
    -------
    Literal['rock', 'paper', 'scissors']
        A uniformly random move.
    """
    return random.choice(['rock', 'paper', 'scissors'])


def determine_winner(
    player: Literal['rock', 'paper', 'scissors'],
    computer: Literal['rock', 'paper', 'scissors']
) -> Literal['player', 'computer', 'tie']:
    """Determine the winner of a single Rock-Paper-Scissors round.

    Parameters
    ----------
    player : Literal['rock', 'paper', 'scissors']
        Player's move.
    computer : Literal['rock', 'paper', 'scissors']
        Computer's move.

    Returns
    -------
    Literal['player', 'computer', 'tie']
        The round outcome.

    Raises
    ------
    ValueError
        If either argument is not a valid move.

    Examples
    --------
    >>> determine_winner('rock', 'scissors')
    'player'
    >>> determine_winner('paper', 'rock')
    'player'
    >>> determine_winner('rock', 'rock')
    'tie'
    """
    valid = {'rock', 'paper', 'scissors'}
    if player not in valid or computer not in valid:
        raise ValueError(f"Invalid moves: player={player!r}, computer={computer!r}; expected one of {sorted(valid)}")

    if player == computer:
        return 'tie'

    beats = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    return 'player' if beats[player] == computer else 'computer'


class RPSApp:
    """Tkinter GUI for Rock-Paper-Scissors.

    Displays a simple interface with three move buttons, a result label,
    a detailed scoreboard (player/computer/ties), and a scrollable round
    history. Tracks and displays scores across multiple rounds.

    Attributes
    ----------
    root : tk.Tk
        The root window.
    player_score : int
        Number of rounds won by the player.
    computer_score : int
        Number of rounds won by the computer.
    ties : int
        Number of tied rounds.
    round : int
        Total number of rounds played.

    Examples
    --------
    >>> import tkinter as tk
    >>> root = tk.Tk()
    >>> app = RPSApp(root)
    >>> # User can now click buttons. Call root.destroy() to close.
    """

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the RPSApp with a Tkinter root window.

        Parameters
        ----------
        root : tk.Tk
            The root Tkinter window.
        """
        self.root = root
        root.title('Rock Paper Scissors')
        root.resizable(False, False)

        self.player_score = 0
        self.ties = 0
        self.computer_score = 0
        self.round = 0

        self._build_ui()

    def _build_ui(self) -> None:
        """Construct the GUI components.

        Creates the layout: a title label, choice display, three move buttons,
        result label, detailed scoreboard (player/computer/ties), a scrollable
        round history listbox, and Reset/Quit control buttons.

        This method is called once during __init__ and is not typically called
        directly by users.
        """
        pad = 8
        top = tk.Frame(self.root, padx=pad, pady=pad)
        top.pack()

        self.info_label = tk.Label(top, text='Choose your move', font=('Segoe UI', 14))
        self.info_label.pack(pady=(0, 6))

        self.choices_label = tk.Label(top, text='', font=('Segoe UI', 11))
        self.choices_label.pack()

        btn_frame = tk.Frame(top, pady=6)
        btn_frame.pack()

        tk.Button(btn_frame, text='Rock', width=10, command=lambda: self.play('rock')).grid(row=0, column=0, padx=4)
        tk.Button(btn_frame, text='Paper', width=10, command=lambda: self.play('paper')).grid(row=0, column=1, padx=4)
        tk.Button(btn_frame, text='Scissors', width=10, command=lambda: self.play('scissors')).grid(row=0, column=2, padx=4)

        self.result_label = tk.Label(top, text='', font=('Segoe UI', 12, 'bold'))
        self.result_label.pack(pady=(8, 4))

        # Detailed scoreboard: separate labels for player, computer and ties
        score_frame = tk.Frame(top)
        score_frame.pack()

        self.player_score_label = tk.Label(score_frame, text=f'You: {self.player_score}', font=('Segoe UI', 10))
        self.player_score_label.grid(row=0, column=0, padx=8)

        self.computer_score_label = tk.Label(score_frame, text=f'Computer: {self.computer_score}', font=('Segoe UI', 10))
        self.computer_score_label.grid(row=0, column=1, padx=8)

        self.ties_label = tk.Label(score_frame, text=f'Ties: {self.ties}', font=('Segoe UI', 10))
        self.ties_label.grid(row=0, column=2, padx=8)

        # Round history (detailed per-round scoreboard)
        history_frame = tk.Frame(top)
        history_frame.pack(pady=(6, 0), fill=tk.BOTH)

        tk.Label(history_frame, text='Round History', font=('Segoe UI', 10, 'underline')).pack(anchor='w')
        hist_box_frame = tk.Frame(history_frame)
        hist_box_frame.pack(fill=tk.BOTH)

        self.history_listbox = tk.Listbox(hist_box_frame, width=64, height=8)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        hist_scroll = tk.Scrollbar(hist_box_frame, orient=tk.VERTICAL, command=self.history_listbox.yview)
        hist_scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=hist_scroll.set)

        ctrl_frame = tk.Frame(top, pady=6)
        ctrl_frame.pack()
        tk.Button(ctrl_frame, text='Reset', command=self.reset_scores).grid(row=0, column=0, padx=6)
        tk.Button(ctrl_frame, text='Quit', command=self.root.destroy).grid(row=0, column=1, padx=6)

    def _score_text(self):
        return f'Score — You: {self.player_score}   Computer: {self.computer_score}'

    def play(self, player_choice: Literal['rock', 'paper', 'scissors']) -> None:
        """Execute one round of the game.

        Prompts the computer to select a move, determines the winner,
        increments the round counter, updates the scoreboard, and appends
        a history entry.

        Parameters
        ----------
        player_choice : Literal['rock', 'paper', 'scissors']
            The player's move. Must be one of the three valid moves.

        Raises
        ------
        ValueError
            If player_choice is not a valid move (propagated from determine_winner).
        """
        computer_choice = get_computer_choice()
        winner = determine_winner(player_choice, computer_choice)

        self.choices_label.config(text=f'You chose: {player_choice}    Computer chose: {computer_choice}')

        # update round counter and scoreboard
        self.round += 1
        if winner == 'player':
            self.player_score += 1
            self.result_label.config(text='You win!', fg='green')
            outcome_text = 'Player'
        elif winner == 'computer':
            self.computer_score += 1
            self.result_label.config(text='Computer wins!', fg='red')
            outcome_text = 'Computer'
        else:
            self.ties += 1
            self.result_label.config(text="It's a tie!", fg='gray')
            outcome_text = 'Tie'

        # update labels
        self.player_score_label.config(text=f'You: {self.player_score}')
        self.computer_score_label.config(text=f'Computer: {self.computer_score}')
        self.ties_label.config(text=f'Ties: {self.ties}')

        # append round to history
        self.history_listbox.insert(tk.END, f'Round {self.round}: You={player_choice}  Computer={computer_choice}  => {outcome_text}')
        # auto-scroll to last
        self.history_listbox.yview_moveto(1.0)

    def reset_scores(self) -> None:
        """Reset all scores and round history.

        Clears player wins, computer wins, ties, the round counter, all UI labels,
        and the round history listbox. Called when the user clicks the Reset button.
        """
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.round = 0
        self.player_score_label.config(text=f'You: {self.player_score}')
        self.computer_score_label.config(text=f'Computer: {self.computer_score}')
        self.ties_label.config(text=f'Ties: {self.ties}')
        self.choices_label.config(text='')
        self.result_label.config(text='')
        # clear history
        self.history_listbox.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = RPSApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()

