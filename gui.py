"""
gui.py

Tkinter graphical user interface for the Spot the Difference game.
"""

import tkinter as tk
from tkinter import filedialog, messagebox

from game_controller import GameController


class SpotDifferenceGUI:
    """
    Creates and manages the Tkinter user interface.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Spot the Difference Game")
        self.root.geometry("1150x700")
        self.root.resizable(True, True)

        self.controller = GameController()

        self.original_photo = None
        self.modified_photo = None

        self._build_layout()

    def _build_layout(self):
        """
        Build all GUI widgets.
        """

        title_label = tk.Label(
            self.root,
            text="Spot the Difference Game",
            font=("Arial", 20, "bold"),
        )
        title_label.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        load_button = tk.Button(
            button_frame,
            text="Load Image",
            width=15,
            command=self.load_image,
        )
        load_button.grid(row=0, column=0, padx=10)

        reveal_button = tk.Button(
            button_frame,
            text="Reveal Differences",
            width=18,
            command=self.reveal_differences,
        )
        reveal_button.grid(row=0, column=1, padx=10)

        self.status_label = tk.Label(
            self.root,
            text="Load an image to start the game.",
            font=("Arial", 12),
        )
        self.status_label.pack(pady=5)

        self.score_label = tk.Label(
            self.root,
            text="Remaining: 5 | Mistakes: 0/3",
            font=("Arial", 12, "bold"),
        )
        self.score_label.pack(pady=5)

        image_frame = tk.Frame(self.root)
        image_frame.pack(pady=10)

        original_frame = tk.Frame(image_frame)
        original_frame.grid(row=0, column=0, padx=15)

        modified_frame = tk.Frame(image_frame)
        modified_frame.grid(row=0, column=1, padx=15)

        original_title = tk.Label(
            original_frame,
            text="Original Image",
            font=("Arial", 13, "bold"),
        )
        original_title.pack()

        modified_title = tk.Label(
            modified_frame,
            text="Modified Image - Click Here",
            font=("Arial", 13, "bold"),
        )
        modified_title.pack()

        self.original_image_label = tk.Label(
            original_frame,
            text="No image loaded",
            relief="solid",
        )
        self.original_image_label.pack(pady=5)

        self.modified_image_label = tk.Label(
            modified_frame,
            text="No image loaded",
            relief="solid",
        )
        self.modified_image_label.pack(pady=5)

        self.modified_image_label.bind("<Button-1>", self.handle_image_click)

    def load_image(self):
        """
        Open file dialog and load selected image.
        """

        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("BMP Files", "*.bmp"),
            ],
        )

        if not file_path:
            return

        try:
            self.controller.load_new_game(file_path)
            self.refresh_images()
            self.update_status("New game loaded. Find all 5 differences.")

        except ValueError as error:
            messagebox.showerror("Image Loading Error", str(error))

    def handle_image_click(self, event):
        """
        Handle mouse click on modified image.
        """

        success, message, _ = self.controller.process_click(event.x, event.y)

        if self.controller.image_loaded:
            self.refresh_images()

        self.update_status(message)

        if success and self.controller.remaining_differences == 0:
            messagebox.showinfo(
                "Game Completed",
                "Congratulations! You found all five differences.",
            )

        if self.controller.game_over and self.controller.mistakes >= 3:
            messagebox.showwarning(
                "Game Over",
                "You made 3 incorrect attempts. The game is now locked.",
            )

    def reveal_differences(self):
        """
        Reveal all remaining differences.
        """

        if not self.controller.image_loaded:
            messagebox.showinfo("No Image", "Please load an image first.")
            return

        self.controller.reveal_all_differences()
        self.refresh_images()
        self.update_status("All remaining differences have been revealed.")

    def refresh_images(self):
        """
        Refresh displayed images after game state changes.
        """

        original, modified = self.controller.image_processor.prepare_display_images()

        self.original_photo = original
        self.modified_photo = modified

        self.original_image_label.config(image=self.original_photo, text="")
        self.modified_image_label.config(image=self.modified_photo, text="")

        self.update_score_label()

    def update_status(self, message):
        """
        Update status message.
        """

        self.status_label.config(text=message)
        self.update_score_label()

    def update_score_label(self):
        """
        Update score and mistake display.
        """

        status = self.controller.get_game_status()

        self.score_label.config(
            text=(
                f"Remaining: {status['remaining_differences']} | "
                f"Mistakes: {status['mistakes']}/3"
            )
        )