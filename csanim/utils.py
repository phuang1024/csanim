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
Utilities for internal use.
"""

import sys
import os
import shutil
import time
import ctypes
import numpy as np
from numpy import ctypeslib
from typing import Tuple

PARENT = os.path.dirname(os.path.realpath(__file__))
FONTS = os.path.join(PARENT, "fonts")
ROBOTO = os.path.join(FONTS, "roboto_mono.ttf")

AR_FLAGS = "aligned, c_contiguous"
AR3D = ctypeslib.ndpointer(dtype=np.uint8, ndim=3, flags=AR_FLAGS)
UINT = ctypes.c_uint32
DOUB = ctypes.c_double


def empty(resolution: Tuple[int, int], dtype=np.uint8) -> np.ndarray:
    """
    Generates empty numpy array with the given dimensions.
    Reverses given resolution because cv2 uses (height, width) shape.

    :param resolution: (W, H) resolution.
    :param dtype: Data type for np array.
    """
    return np.zeros((*resolution[::-1], 3), dtype=np.uint8)

def getres(img: np.ndarray) -> Tuple[int, int]:
    """
    Gets (W, H) resolution from an image.

    :param img: The image.
    """
    return img.shape[:2][::-1]


class ProgressLogger:
    def __init__(self, msg, total):
        self.msg = msg
        self.total = total
        self.frame = 0
        self.start = time.time()

    @staticmethod
    def _truncate(value, digits=4):
        s = str(value)
        parts = s.split(".")

        if len(parts[0]) > digits or len(parts[0]) == digits-1:
            return parts[0]
        return s[:digits]

    @staticmethod
    def _fit(msg, width=None):
        if width is None:
            width = shutil.get_terminal_size()[0]

        if len(msg) < width:
            return msg
        else:
            return msg[:width-4] + "..."

    def log(self):
        frame = self.frame
        total = self.total

        elapse = time.time() - self.start
        per_second = (frame+1) / elapse
        percent = (frame+1) / total * 100
        remaining = (total-frame-1) / per_second

        msg = f"{self.msg} {frame+1}/{total}, {self._truncate(per_second)} fps, {self._truncate(percent)}% done, " + \
            f"{self._truncate(elapse)}s elapsed, {self._truncate(remaining)}s remaining"
        msg = self._fit(msg)
        log(msg, clear=True)

    def finish(self, msg):
        elapse = time.time() - self.start
        log(msg.replace("$TIME", str(elapse)[:4]), clear=True, new=True)

    def update(self, frame):
        self.frame = frame


def log(msg, clear=False, new=False, flush=True):
    if clear:
        clearline(flush=False)
    sys.stdout.write(msg)
    if flush and not new:
        sys.stdout.flush()
    if new:
        newline(flush=flush)

def clearline(flush=True):
    width = shutil.get_terminal_size()[0]
    sys.stdout.write("\r")
    sys.stdout.write(" "*width)
    sys.stdout.write("\r")
    if flush:
        sys.stdout.flush()

def newline(flush=True):
    sys.stdout.write("\n")
    if flush:
        sys.stdout.flush()


def bounds(v: float, vmin: float = 0, vmax: float = 1):
    return max(min(v, vmax), vmin)


def loading():
    while True:
        yield from "-\\|/"
