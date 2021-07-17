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

import numpy as np
from typing import Tuple
from .props import *
from . import lib


class Element:
    show: BoolProp

    def __init__(self) -> None:
        self.show = BoolProp(True)

    def render(self, img: np.ndarray, frame: float) -> None:
        ...


class Circle(Element):
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

    def render(self, img: np.ndarray, frame: float) -> None:
        color = self.color.value(frame)
        center = self.center.value(frame)
        radius = self.radius.value(frame)
        border = self.border.value(frame)
        lib.draw.circle(img, color, center, radius, border)


class Rect(Element):
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

    def render(self, img: np.ndarray, frame: float) -> None:
        color = self.color.value(frame)
        loc = self.loc.value(frame)
        size = self.size.value(frame)
        border = self.border.value(frame)
        border_radius = self.border_radius.value(frame)
        lib.draw.rect(img, color, (*loc, *size), border, border_radius)
