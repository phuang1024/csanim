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

from typing import List, Tuple
from .scene import Scene


class Video:
    """
    Base video class.
    """
    fps: int
    resolution: Tuple[int, int]
    scenes: List[Scene]

    def __init__(self, fps: int, resolution: Tuple[int, int]) -> None:
        """
        Initializes video.
        :param fps: Frames per second of video.
        :param resolution: (x, y) pixel resolution.
        """
        self.fps = fps
        self.resolution = resolution
        self.scenes = []

    def __repr__(self) -> str:
        return f"<csanim.Video(nscenes={len(self.scenes)}>"

    def __str__(self) -> str:
        return repr(self)

    def add_scene(self, scene: Scene):
        self.scenes.append(scene)
