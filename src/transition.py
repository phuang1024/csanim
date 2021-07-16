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
from .constants import *
from .utils import bounds


def cut(img1, img2, fac):
    return img1 if fac < 0 else img2


def fade(img1, img2, fac):
    fac1 = bounds((1-fac)/2)
    fac2 = bounds((1+fac)/2)
    return img1*fac1 + img2*fac2


def fadeio(img1, img2, fac):
    fac1 = bounds(-fac)
    fac2 = bounds(fac)
    return img1*fac1 + img2*fac2


def transition(img1: np.ndarray, img2: np.ndarray, fac: float, mode: int) -> np.ndarray:
    """
    Transitions two images.
    :param img1: Image 1
    :param img2: Image 2
    :param fac: Factor of transition. -1 = full img1, 1 = full img2
    :param mode: Transition mode, found in csanim.constants
    """
    if mode == TR_CUT:
        return cut(img1, img2, fac)
    elif mode == TR_FADE:
        return fade(img1, img2, fac)
    elif mode == TR_FADEIO:
        return fadeio(img1, img2, fac)
    raise NotImplementedError
