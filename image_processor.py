"""
image_processor.py

Handles image loading, validation, resizing, and random difference generation.
"""

import random

import cv2
import numpy as np
from PIL import Image, ImageTk

from models import (
    DifferenceRegion,
    BrightnessAlteration,
    BlurAlteration,
    ColorShiftAlteration,
)


class ImageProcessor:
    """
    Responsible for loading images and creating modified copies.
    """

    def __init__(self):
        self.original_image = None
        self.modified_image = None
        self.display_original = None
        self.display_modified = None
        self.scale_factor = 1.0
        self.regions = []

        self.alterations = [
            BrightnessAlteration(),
            BlurAlteration(),
            ColorShiftAlteration(),
        ]

    def load_image(self, file_path):
        """
        Load an image safely using OpenCV.

        Args:
            file_path (str): Image file path

        Raises:
            ValueError: If image cannot be loaded or is too small
        """

        image = cv2.imread(file_path)

        if image is None:
            raise ValueError("The selected file could not be loaded as an image.")

        height, width = image.shape[:2]

        if width < 300 or height < 200:
            raise ValueError("Image is too small. Please choose a larger image.")

        self.original_image = image
        self.modified_image = image.copy()
        self.regions = []

        self._create_random_differences()

    def _create_random_differences(self):
        """
        Create exactly five non-overlapping random differences.
        """

        height, width = self.original_image.shape[:2]

        max_attempts = 1000
        attempts = 0

        while len(self.regions) < 5 and attempts < max_attempts:
            attempts += 1

            region_width = random.randint(55, 90)
            region_height = random.randint(55, 90)

            x = random.randint(10, width - region_width - 10)
            y = random.randint(10, height - region_height - 10)

            new_region = DifferenceRegion(x, y, region_width, region_height)

            if not self._has_overlap(new_region) and self._is_region_bright_enough(new_region):
                alteration = random.choice(self.alterations)

                before_region = self.modified_image[
                    new_region.y:new_region.y + new_region.height,
                    new_region.x:new_region.x + new_region.width
                ].copy()

                alteration.apply(self.modified_image, new_region)

                after_region = self.modified_image[
                    new_region.y:new_region.y + new_region.height,
                    new_region.x:new_region.x + new_region.width
                ]

                difference_score = np.mean(
                    cv2.absdiff(before_region, after_region)
                )

                if difference_score >= 14:
                    self.regions.append(new_region)
                else:
                    self.modified_image[
                        new_region.y:new_region.y + new_region.height,
                        new_region.x:new_region.x + new_region.width
                    ] = before_region

        if len(self.regions) != 5:
            raise ValueError("Could not create five safe non-overlapping differences.")

    def _is_region_bright_enough(self, region, minimum_brightness=55):
        """
        Check whether a region is bright enough for visible soft alterations.
        """

        roi = self.original_image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ]

        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        average_brightness = np.mean(gray_roi)

        return average_brightness >= minimum_brightness

    def _has_overlap(self, new_region):
        """
        Check if a new region overlaps existing regions.
        """

        padding = 15

        padded_region = DifferenceRegion(
            new_region.x - padding,
            new_region.y - padding,
            new_region.width + padding * 2,
            new_region.height + padding * 2,
        )

        for region in self.regions:
            if padded_region.overlaps(region):
                return True

        return False

    def prepare_display_images(self, max_width=500, max_height=500):
        """
        Resize images for Tkinter display while preserving aspect ratio.

        Returns:
            tuple: Tkinter-compatible original and modified images
        """

        height, width = self.original_image.shape[:2]

        width_scale = max_width / width
        height_scale = max_height / height
        self.scale_factor = min(width_scale, height_scale)

        if self.scale_factor <= 0:
            self.scale_factor = 1.0

        display_width = int(width * self.scale_factor)
        display_height = int(height * self.scale_factor)

        original_resized = cv2.resize(
            self.original_image,
            (display_width, display_height),
            interpolation=cv2.INTER_AREA,
        )

        modified_resized = cv2.resize(
            self.modified_image,
            (display_width, display_height),
            interpolation=cv2.INTER_AREA,
        )

        original_rgb = cv2.cvtColor(original_resized, cv2.COLOR_BGR2RGB)
        modified_rgb = cv2.cvtColor(modified_resized, cv2.COLOR_BGR2RGB)

        self.display_original = ImageTk.PhotoImage(Image.fromarray(original_rgb))
        self.display_modified = ImageTk.PhotoImage(Image.fromarray(modified_rgb))

        return self.display_original, self.display_modified

    def display_to_original_coordinates(self, display_x, display_y):
        """
        Convert displayed click coordinates back to original image coordinates.
        """

        original_x = int(display_x / self.scale_factor)
        original_y = int(display_y / self.scale_factor)

        return original_x, original_y

    def draw_found_region(self, region):
        """
        Draw red circles around a found difference on both images.
        """

        center_x = region.x + region.width // 2
        center_y = region.y + region.height // 2
        radius = max(region.width, region.height) // 2

        cv2.circle(self.original_image, (center_x, center_y), radius, (0, 0, 255), 3)
        cv2.circle(self.modified_image, (center_x, center_y), radius, (0, 0, 255), 3)

    def draw_reveal_region(self, region):
        """
        Draw blue circles around unrevealed/unfound differences.
        """

        center_x = region.x + region.width // 2
        center_y = region.y + region.height // 2
        radius = max(region.width, region.height) // 2

        cv2.circle(self.original_image, (center_x, center_y), radius, (255, 0, 0), 3)
        cv2.circle(self.modified_image, (center_x, center_y), radius, (255, 0, 0), 3)

    def draw_wrong_click(self, x, y):
        """
        Draw an orange X marker on the modified image for an incorrect click.
        """

        marker_size = 15
        color = (40, 0, 120)
        thickness = 4

        cv2.line(
            self.modified_image,
            (x - marker_size, y - marker_size),
            (x + marker_size, y + marker_size),
            color,
            thickness
        )

        cv2.line(
            self.modified_image,
            (x + marker_size, y - marker_size),
            (x - marker_size, y + marker_size),
            color,
            thickness
        )


def _is_region_bright_enough(self, region, minimum_brightness=70):
    """
    Check whether a region is bright enough for visible soft alterations.
    """

    roi = self.original_image[
        region.y:region.y + region.height,
        region.x:region.x + region.width
    ]

    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    average_brightness = np.mean(gray_roi)

    return average_brightness >= minimum_brightness