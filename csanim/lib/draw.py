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
Module for graphical drawing functions.
"""

import os
import ctypes
import numpy as np
from numpy import ctypeslib as ctl
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Union
from ..constants import *
from ..utils import *

lib = ctypes.CDLL(os.path.join(PARENT, "libdraw.so"))
lib.line.argtypes = [AR3D, UINT, UINT, *[DOUB for _ in range(9)]]
lib.circle.argtypes = [AR3D, UINT, UINT, *[DOUB for _ in range(8)]]
lib.rect.argtypes = [AR3D, UINT, UINT, *[DOUB for _ in range(14)]]
lib.arrow.argtypes = [AR3D, UINT, UINT, *[DOUB for _ in range(11)]]


def rgba(color):
    return (*color, 255) if len(color) == 3 else color


def line(img: np.ndarray, color: Tuple[float, ...], p1: Tuple[float, float], p2: Tuple[float, float],
        thickness: float = 1) -> None:
    """
    Draws a line.

    :param img: Image.
    :param color: RGB or RGBA color.
    :param p1: (X, Y) of point 1.
    :param p2: (X, Y) of point 2.
    :param thickness: Line thickness.
    """
    assert img.dtype == np.uint8
    color = rgba(color)
    lib.line(img, img.shape[1], img.shape[0], *p1, *p2, thickness, *color)


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
    color = rgba(color)
    lib.circle(img, img.shape[1], img.shape[0], *center, radius, border, *color)


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
    color = rgba(color)
    lib.rect(img, img.shape[1], img.shape[0], *dims, border, border_radius, tl_rad, tr_rad, bl_rad, br_rad, *color)


def arrow(img: np.ndarray, color: Tuple[float, ...], tail: Tuple[float, float], head: Tuple[float, float],
        angle: float = 40, side_len_fac: float = 0.4, thickness: float = 1):
    """
    Draws an arrow.

    :param img: Image.
    :param color: RGB or RGBA color.
    :param tail: (X, Y) location of the arrow's tail.
    :param head: (X, Y) location of head (where the three lines meet).
    :param angle: Angle between main line and side lines (degrees).
    :param side_len_fac: Length factor of side lines.
    :param thickness: Thickness.
    """
    assert img.dtype == np.uint8
    color = rgba(color)
    lib.arrow(img, img.shape[1], img.shape[0], *tail, *head, angle, side_len_fac, thickness, *color)


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
