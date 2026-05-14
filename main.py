"""
main.py

Entry point for the Spot the Difference game.
"""

import tkinter as tk

from gui import SpotDifferenceGUI


def main():
    """
    Start the Tkinter application.
    """

    root = tk.Tk()
    SpotDifferenceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()