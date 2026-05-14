"""
models.py

This file contains the core data models and image alteration classes
for the Spot the Difference game.
"""

from abc import ABC, abstractmethod

import cv2


class DifferenceRegion:
    """
    Stores information about one difference region.
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.found = False
        self.revealed = False

    def contains_point(self, px, py):
        """
        Check if a point is inside the region.
        """

        return (
            self.x <= px <= self.x + self.width
            and self.y <= py <= self.y + self.height
        )

    def overlaps(self, other_region):
        """
        Check if this region overlaps another region.
        """

        return not (
            self.x + self.width < other_region.x
            or other_region.x + other_region.width < self.x
            or self.y + self.height < other_region.y
            or other_region.y + other_region.height < self.y
        )


class ImageAlteration(ABC):
    """
    Abstract parent class for image alterations.

    Used to demonstrate inheritance and polymorphism.
    """

    @abstractmethod
    def apply(self, image, region):
        pass


class BrightnessAlteration(ImageAlteration):
    """
    Makes the selected region clearly brighter.
    """

    def apply(self, image, region):

        roi = image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ]

        roi[:] = cv2.convertScaleAbs(roi, alpha=1.0, beta=75)


class BlurAlteration(ImageAlteration):
    """
    Applies a strong blur effect to a selected region.
    """

    def apply(self, image, region):

        roi = image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ]

        blurred = cv2.GaussianBlur(roi, (25, 25), 0)

        image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ] = blurred


class ColorShiftAlteration(ImageAlteration):
    """
    Applies a visible colour shift to a selected region.
    """

    def apply(self, image, region):

        roi = image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ]

        shifted = roi.copy()
        shifted[:, :, 0] = cv2.add(shifted[:, :, 0], 80)
        shifted[:, :, 1] = cv2.subtract(shifted[:, :, 1], 60)

        image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ] = shifted


class ShapeAlteration(ImageAlteration):
    """
    Adds a small visible shape inside the selected region.
    This guarantees the difference can be detected by the player.
    """

    def apply(self, image, region):

        center_x = region.x + region.width // 2
        center_y = region.y + region.height // 2
        radius = min(region.width, region.height) // 4

        cv2.circle(
            image,
            (center_x, center_y),
            radius,
            (0, 255, 255),
            -1
        )
