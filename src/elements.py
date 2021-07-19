#
#  CS Animation
#  A tool for creating computer science explanatory videos.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""
Simple animatable elements that build scenes.
"""

__all__ = (
    "Element",
    "Fill",
    "Circle",
    "Rect",
)

import numpy as np
from typing import Tuple
from .props import *
from .lib import draw


class Element:
    """
    Base element class. All other elements inherit from this.
    """
    show: BoolProp

    def __init__(self) -> None:
        """
        All inherited classes should call super().__init__()
        Sets the "show" prop.
        """
        self.show = BoolProp(True)

    def relevant(self, frame: float) -> bool:
        """
        Elements can define their own implementation.
        Decides whether the element is worth rendering (e.g. color is not transparent)
        :param frame: The frame in question.
        """
        return True

    def render(self, img: np.ndarray, frame: float) -> None:
        """
        Elements define their own implementation.
        Modify the input array in place.
        :param img: Numpy array image.
        :param frame: Frame.
        """


class Fill(Element):
    """
    Fills the whole scene with one color.
    Use alpha to control visibility of elements behind it.

    Animatable attributes:
    * color: The RGBA color to fill.
    """
    color: VectorProp

    def __init__(self, color: Tuple[float, ...] = (0, 0, 0, 255)) -> None:
        super().__init__()
        self.color = VectorProp(FloatProp, 4, color)

    def relevant(self, frame: float) -> bool:
        color = self.color.value(frame)
        return color[3] != 0

    def render(self, img: np.ndarray, frame: float) -> None:
        color = self.color.value(frame)
        alpha = color[-1] / 255

        fill = np.full(img.shape, color[:3], dtype=np.uint8)
        new = fill*alpha + img*(1-alpha)

        img[:] = new


class Circle(Element):
    """
    Draws a circle.

    Animatable attributes:
    * color: The RGBA color.
    * center: (X, Y) center location.
    * radius: Radius of the circle.
    * border: Border thickness.
    """
    color: VectorProp
    center: VectorProp
    radius: FloatProp
    border: FloatProp

    def __init__(self, color: Tuple[float, ...] = (255, 255, 255, 255), center: Tuple[float, float] = (0, 0),
            radius: float = 100, border: float = 0) -> None:
        super().__init__()
        self.color = VectorProp(FloatProp, 4, color)
        self.center = VectorProp(FloatProp, 2, center)
        self.radius = FloatProp(radius)
        self.border = FloatProp(border)

    def relevant(self, frame: float) -> bool:
        color = self.color.value(frame)
        return color[3] != 0

    def render(self, img: np.ndarray, frame: float) -> None:
        color = self.color.value(frame)
        center = self.center.value(frame)
        radius = self.radius.value(frame)
        border = self.border.value(frame)
        draw.circle(img, color, center, radius, border)


class Rect(Element):
    """
    Draws a rectangle.

    Animatable attributes:
    * color: The RGBA color.
    * loc: (X, Y) top left corner location.
    * size: (width, height) size.
    * border: Border thickness.
    * border_radius: Corner rounding radius.
    """
    color: VectorProp
    loc: VectorProp
    size: VectorProp
    border: FloatProp
    border_radius: FloatProp

    def __init__(self, color: Tuple[float, ...] = (255, 255, 255, 255), loc: Tuple[float, float] = (0, 0),
            size: Tuple[float, float] = (0, 0), border: float = 0, border_radius: float = 0) -> None:
        super().__init__()
        self.color = VectorProp(FloatProp, 4, color)
        self.loc = VectorProp(FloatProp, 2, loc)
        self.size = VectorProp(FloatProp, 2, size)
        self.border = FloatProp(border)
        self.border_radius = FloatProp(border_radius)

    def relevant(self, frame: float) -> bool:
        color = self.color.value(frame)
        return color[3] != 0

    def render(self, img: np.ndarray, frame: float) -> None:
        color = self.color.value(frame)
        loc = self.loc.value(frame)
        size = self.size.value(frame)
        border = self.border.value(frame)
        border_radius = self.border_radius.value(frame)
        draw.rect(img, color, (*loc, *size), border, border_radius)
