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
Module for interpolation functions.
"""

import os
import ctypes
from ..constants import *
from ..utils import *

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
    return lib.linear(f1, f2, v1, v2, frame)

@staticmethod
def sine(f1, f2, v1, v2, frame):
    """
    Sine interpolation.
    """
    return lib.sine(f1, f2, v1, v2, frame)
