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
Scenes. A scene is a section of a video.
The base scene exists (just a collection of elements).
More complex scenes also exist.
"""

__all__ = [
    "Scene",
    "SceneCode",
]

import numpy as np
from typing import List, Tuple, Union
from .constants import *
from .elements import *
from .lib import draw
from .props import *
from .transition import transition


def _empty(resolution: Tuple[int, int]) -> np.ndarray:
    return np.zeros((*resolution[::-1], 3), dtype=np.uint8)


class Scene:
    """
    Base scene.
    When defining your own scene, inherit from this.
    """
    length: float   # seconds
    trans_start: int
    trans_len: float
    elements: List[Element]

    def __init__(self, length: float, trans_start: int = T_CUT, trans_len: float = 1.5):
        """
        Initializes scene.
        :param length: Length IN SECONDS
        TODO transitions not implemented yet
        """
        self.length = length
        self.trans_start = trans_start
        self.trans_len = trans_len
        self.elements = []

    def add_element(self, element: Element) -> None:
        """
        Appends an element to the internal list.
        This element will go above any previous elements.
        """
        self.elements.append(element)

    def render(self, resolution: Tuple[int, int], frame: float, fps: int) -> np.ndarray:
        """
        Renders an image. Define your own implementation if you are inheriting.
        Return a numpy array image.
        Make sure the array's shape is (H, W).
        :param resolution: (X, Y) resolution.
        :param frame: Frame.
        :param fps: FPS.
        """
        img = _empty(resolution)
        for element in self.elements:
            if element.show.value(frame) and element.relevant(frame):
                element.render(img, frame)
        # TODO transition
        return img


class SceneCode(Scene):
    """
    A scene with code text.
    Simple interface: typewrite() writes the text, etc.
    Still in development.
    """
    font: StrProp
    font_size: IntProp
    char_width: IntProp

    def __init__(self, font: Union[int, str] = F_CODE, font_size: int = 14, char_width: int = 8,
            init_text: str = "") -> None:
        self.font = StrProp(font)
        self.font_size = IntProp(font_size)
        self.char_width = IntProp(char_width)

        self._time = 0
        self._max_time = 0
        self._text = StrProp("")   # THIS PROP STORES KEYFRAMES IN SECONDS
        self._cursor = VectorProp(IntProp, 2, (0, 0))   # THIS PROP STORES KEYFRAMES IN SECONDS

        self._text.key(0, init_text)

    @property
    def length(self):
        return self._max_time

    def wait(self, time: float) -> float:
        self._time += time
        self._max_time = max(self._time, self._max_time)
        return self._time

    def typewrite(self, text: str, delay: float = 0.08) -> float:
        for char in text:
            self._time += delay

            value = self._text.value(self._time)
            cursor = self._cursor.value(self._time)
            new_cursor = [cursor[0]+1, cursor[1]]

            self._text.key(self._time, value+char)
            self._cursor.key(self._time, cursor)
            self._cursor.key(self._time+min(delay, 0.05), new_cursor)

        self._time += delay
        self._max_time = max(self._time, self._max_time)
        return self._time

    def render(self, resolution: Tuple[int, int], frame: float, fps: int) -> np.ndarray:
        text = self._text.value(frame/fps)
        char_width = self.char_width.value(frame)
        font = self.font.value(frame)
        font_size = self.font_size.value(frame)
        cursor = self._cursor.value(frame/fps)

        img = _empty(resolution)

        for i, char in enumerate(text):
            x = char_width * i
            draw.text(img, (255, 255, 255), (x, 1), char, font, font_size)

        cursor_x = cursor[0] * char_width
        draw.rect(img, (255, 255, 255), (cursor_x, 0, 1, 20))

        return img
