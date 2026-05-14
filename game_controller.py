"""
game_controller.py

Controls game logic and state management.
"""

from image_processor import ImageProcessor


class GameController:
    """
    Controls the game flow and rules.
    """

    MAX_MISTAKES = 3

    def __init__(self):
        """
        Initialize game controller.
        """

        self.image_processor = ImageProcessor()

        self.remaining_differences = 5
        self.mistakes = 0
        self.game_over = False
        self.image_loaded = False

    def load_new_game(self, file_path):
        """
        Load a new image and reset the game state.

        Args:
            file_path (str): Path to image file
        """

        self.image_processor.load_image(file_path)

        self.remaining_differences = 5
        self.mistakes = 0
        self.game_over = False
        self.image_loaded = True

    def process_click(self, display_x, display_y):
        """
        Process a player's click.

        Args:
            display_x (int): Click x-coordinate on displayed image
            display_y (int): Click y-coordinate on displayed image

        Returns:
            tuple:
                (success, message, region_found)
        """

        if not self.image_loaded:
            return False, "Please load an image first.", None

        if self.game_over:
            return False, "Game is already over.", None

        original_x, original_y = (
            self.image_processor.display_to_original_coordinates(
                display_x,
                display_y
            )
        )
        
        if original_x < 0 or original_y < 0:
            return False, "Invalid click position.", None
        
        height, width = self.image_processor.original_image.shape[:2]

        if original_x >= width or original_y >= height:
            return False, "Click outside image boundaries.", None

        for region in self.image_processor.regions:

            if region.contains_point(original_x, original_y):

                if region.found:
                    return False, "Difference already found.", None

                region.found = True

                self.image_processor.draw_found_region(region)

                self.remaining_differences -= 1

                if self.remaining_differences == 0:
                    self.game_over = True
                    return True, "Congratulations! You found all differences.", region

                return True, "Correct difference found.", region

        self.mistakes += 1

        if self.mistakes >= self.MAX_MISTAKES:
            self.game_over = True

            return (
                False,
                "Game over. Maximum mistakes reached.",
                None,
            )

        remaining_attempts = self.MAX_MISTAKES - self.mistakes

        return (
            False,
            f"Incorrect click. {remaining_attempts} attempts remaining.",
            None,
        )

    def reveal_all_differences(self):
        """
        Reveal all unfound differences.
        """

        if not self.image_loaded:
            return

        for region in self.image_processor.regions:

            if not region.found:

                region.revealed = True

                self.image_processor.draw_reveal_region(region)

        self.remaining_differences = 0
        self.game_over = True

    def get_game_status(self):
        """
        Get current game status.

        Returns:
            dict: Game state information
        """

        return {
            "remaining_differences": self.remaining_differences,
            "mistakes": self.mistakes,
            "game_over": self.game_over,
            "image_loaded": self.image_loaded,
        }