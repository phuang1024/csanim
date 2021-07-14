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

import os
import ctypes
import numpy as np
from numpy import ctypeslib as ctl

PARENT = os.path.dirname(os.path.realpath(__file__))
AR_FLAGS = "aligned, c_contiguous"


class draw:
    lib = ctypes.CDLL(os.path.join(PARENT, "libdraw.so"))
    lib.circle.argtypes = [
        ctl.ndpointer(dtype=np.uint8, ndim=3, flags=AR_FLAGS),
        ctypes.c_uint32,
        ctypes.c_uint32
    ]

    @staticmethod
    def circle(img: np.ndarray):
        assert img.dtype == np.uint8
        draw.lib.circle(img, img.shape[1], img.shape[0])
