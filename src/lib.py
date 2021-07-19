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
Loads and handles Shared Object libraries.
"""

import os
import ctypes
import numpy as np
from typing import Tuple, Union
from numpy import ctypeslib as ctl
from PIL import Image, ImageFont, ImageDraw
from .constants import *

PARENT = os.path.dirname(os.path.realpath(__file__))
FONTS = os.path.join(PARENT, "fonts")
ROBOTO = os.path.join(FONTS, "roboto_mono.ttf")

AR_FLAGS = "aligned, c_contiguous"
UINT = ctypes.c_uint32
DOUB = ctypes.c_double


class draw:
    """
    Namespace for graphical drawing functions.
    """
    lib = ctypes.CDLL(os.path.join(PARENT, "libdraw.so"))
    lib.circle.argtypes = [
        ctl.ndpointer(dtype=np.uint8, ndim=3, flags=AR_FLAGS),
        UINT, UINT, *[DOUB for _ in range(8)]
    ]
    lib.rect.argtypes = [
        ctl.ndpointer(dtype=np.uint8, ndim=3, flags=AR_FLAGS),
        UINT, UINT, *[DOUB for _ in range(14)]
    ]

    @staticmethod
    def circle(img: np.ndarray, color: Tuple[float, ...], center: Tuple[float, float],
            radius: float, border: float = 0):
        """
        Draws a circle.
        :param img: Image.
        :param color: RGB or RGBA color.
        :param center: (X, Y) center.
        :param radius: Radius.
        :param border: Border thickness. Set to 0 for no border.
        """
        assert img.dtype == np.uint8
        color = (*color, 255) if len(color) == 3 else color
        draw.lib.circle(img, img.shape[1], img.shape[0], *center, radius, border, *color)

    @staticmethod
    def rect(img: np.ndarray, color: Tuple[float, ...], dims: Tuple[float, float, float, float],
            border: float = 0, border_radius: float = 0, tl_rad: float = -1, tr_rad: float = -1,
            bl_rad: float = -1, br_rad: float = -1) -> None:
        """
        Draws a rectangle.
        :param img: Image.
        :param color: RGB or RGBA color.
        :param dims: (X, Y, W, H) dimensions.
        :param border: Border thickness.
        :param border_radius: Corner rounding radius.
        :param tl_rad: Top left corner radius.
        :param tr_rad: Top right corner radius.
        :param bl_rad: Bottom left corner radius.
        :param br_rad: Bottom right corner radius.
        """
        assert img.dtype == np.uint8
        color = (*color, 255) if len(color) == 3 else color
        draw.lib.rect(img, img.shape[1], img.shape[0], *dims, border, border_radius, tl_rad, tr_rad, bl_rad, br_rad, *color)

    @staticmethod
    def text(img: np.ndarray, color: Tuple[float, ...], loc: Tuple[float, float], text: str,
            font: Union[int, str], font_size: int) -> None:
        """
        Draws text.
        :param img: Image.
        :param color: RGB or RGBA color.
        :param loc: (X, Y) location of top left corner.
        :param text: String text to render.
        :param font: Font. Integer = builtin constant (F_CODE), str = font path (/path/a.ttf)
        :param font_size: Font size.
        """
        if isinstance(font, int):
            if font == F_CODE:
                real_font = ImageFont.truetype(ROBOTO, font_size)
            else:
                raise ValueError(f"Invalid font code: {font}")
        else:
            real_font = ImageFont.truetype(font, font_size)

        pil = Image.fromarray(img)
        ImageDraw.Draw(pil).text(loc, text, color[:3][::-1], real_font)
        img[:] = np.array(pil)


class interp:
    """
    Namespace for interpolation functions.
    """
    lib = ctypes.CDLL(os.path.join(PARENT, "libinterp.so"))
    lib.linear.argtypes = [DOUB for _ in range(5)]
    lib.linear.restype = ctypes.c_double
    lib.sine.argtypes = [DOUB for _ in range(5)]
    lib.sine.restype = ctypes.c_double

    @staticmethod
    def constant(f1, f2, v1, v2, frame):
        """
        Constant interpolation.
        Always returns the first value.
        """
        return v1

    @staticmethod
    def linear(f1, f2, v1, v2, frame):
        """
        Linear interpolation.
        """
        return interp.lib.linear(f1, f2, v1, v2, frame)

    @staticmethod
    def sine(f1, f2, v1, v2, frame):
        """
        Sine interpolation.
        """
        return interp.lib.sine(f1, f2, v1, v2, frame)
