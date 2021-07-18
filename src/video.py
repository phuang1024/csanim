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

import sys
import os
import subprocess
import time
import cv2
from typing import List, Tuple
from .scene import Scene
from .utils import loading

FFMPEG = "/usr/bin/ffmpeg"


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

    def add_scene(self, scene: Scene) -> None:
        self.scenes.append(scene)

    def render(self, path: str, vencode: str = "libx265") -> None:
        if os.path.isfile(path) and input(f"Path {path} exists. Overwrite? [y/N] ").strip().lower() != "y":
            return

        dir_path = path + "_imgs"
        os.makedirs(dir_path, exist_ok=True)

        frame = 0
        for scene in self.scenes:
            for f in range(scene.length):
                sys.stdout.write("\r"+" "*80+"\r")
                sys.stdout.write(f"Rendering frame {frame}")
                sys.stdout.flush()

                img = scene.render(self.resolution, f)
                fpath = os.path.join(dir_path, f"{frame}.jpg")
                cv2.imwrite(fpath, img)
                frame += 1

        args = [FFMPEG, "-y", "-i", os.path.join(dir_path, "%d.jpg"), "-c:v", vencode, "-r", str(self.fps), path]
        proc = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        chars = loading()
        while proc.poll() is None:
            sys.stdout.write("\r"+" "*80+"\r")
            sys.stdout.write(f"Compiling images to video...{next(chars)}")
            sys.stdout.flush()
            time.sleep(0.1)

        sys.stdout.write("\r"+" "*80+"\r")
        if proc.returncode == 0:
            print(f"Finished exporting {frame} frames.")
        else:
            print(f"Video compilation failed. Rendered images are in {dir_path}.")
