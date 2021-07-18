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

__all__ = [
    "Scene",
]

import numpy as np
from typing import List, Tuple
from .constants import *
from .transition import transition
from .elements import Element


class Scene:
    length: int
    trans_start: int
    trans_len: float
    elements: List[Element]

    def __init__(self, length: int, trans_start: int = T_CUT, trans_len: float = 1.5):
        self.length = length
        self.trans_start = trans_start
        self.trans_len = trans_len
        self.elements = []

    def add_element(self, element: Element) -> None:
        self.elements.append(element)

    def render(self, resolution: Tuple[int, int], frame: float) -> np.ndarray:
        img = np.zeros((*resolution[::-1], 3), dtype=np.uint8)
        for element in self.elements:
            element.render(img, frame)
        # TODO transition
        return img
