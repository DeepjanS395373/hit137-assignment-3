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
    def apply(self, image, region):
        roi = image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ]
        roi[:] = cv2.convertScaleAbs(roi, alpha=1.06, beta=16)


class BlurAlteration(ImageAlteration):
    def apply(self, image, region):
        roi = image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ]

        blurred = cv2.GaussianBlur(roi, (13, 13), 0)

        image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ] = blurred


class ColorShiftAlteration(ImageAlteration):
    """
    Applies a soft blended colour tint using a faded elliptical mask.
    """

    def apply(self, image, region):

        import random
        import numpy as np

        roi = image[
            region.y:region.y + region.height,
            region.x:region.x + region.width
        ]

        overlay = roi.copy()

        colour_styles = [
            (170, 120, 220),   # purple
            (220, 170, 120),   # warm orange
            (120, 220, 180),   # mint green
            (200, 160, 255),   # pink
            (160, 220, 255),   # cyan
        ]

        tint_colour = random.choice(colour_styles)

        overlay[:] = tint_colour

        mask = np.zeros((region.height, region.width), dtype=np.uint8)

        center = (region.width // 2, region.height // 2)

        axes = (
            int(region.width * 0.35),
            int(region.height * 0.35)
        )

        cv2.ellipse(
            mask,
            center,
            axes,
            0,
            0,
            360,
            255,
            -1
        )

        mask = cv2.GaussianBlur(mask, (31, 31), 0)

        alpha = mask.astype(float) / 255.0
        alpha = alpha[:, :, np.newaxis]

        blended = (
            roi.astype(float) * (1 - alpha)
            + overlay.astype(float) * alpha * 0.25
        )

        roi[:] = blended.astype(np.uint8)
