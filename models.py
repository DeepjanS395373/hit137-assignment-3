"""
models.py

This file contains the core data models and image alteration classes
for the Spot the Difference game.
"""

from abc import ABC, abstractmethod


class DifferenceRegion:
    """
    Stores information about one difference region.
    """

    def __init__(self, x, y, width, height):
        """
        Initialize a difference region.

        Args:
            x (int): Top-left x-coordinate
            y (int): Top-left y-coordinate
            width (int): Region width
            height (int): Region height
        """

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.found = False
        self.revealed = False

    def contains_point(self, px, py):
        """
        Check if a point is inside the region.

        Args:
            px (int): X-coordinate of click
            py (int): Y-coordinate of click

        Returns:
            bool: True if point is inside region
        """

        return (
            self.x <= px <= self.x + self.width
            and self.y <= py <= self.y + self.height
        )

    def overlaps(self, other_region):
        """
        Check if this region overlaps another region.

        Args:
            other_region (DifferenceRegion): Another region object

        Returns:
            bool: True if regions overlap
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
        """
        Apply alteration to the image region.

        Args:
            image: OpenCV image
            region (DifferenceRegion): Region to modify
        """

        pass


class BrightnessAlteration(ImageAlteration):
    """
    Alters image brightness inside a region.
    """

    def apply(self, image, region):

        roi = image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ]

        roi[:] = roi.clip(0, 255) * 0.7


class BlurAlteration(ImageAlteration):
    """
    Applies blur effect to a region.
    """

    def apply(self, image, region):

        import cv2

        roi = image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ]

        blurred = cv2.GaussianBlur(roi, (9, 9), 0)

        image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ] = blurred


class ColorShiftAlteration(ImageAlteration):
    """
    Applies colour shift to a region.
    """

    def apply(self, image, region):

        roi = image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ]

        roi[:, :, 1] = roi[:, :, 1].clip(0, 255) * 0.5