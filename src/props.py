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

__all__ = (
    "VectorProp",
    "BoolProp",
    "IntProp",
    "FloatProp",
    "StrProp",
)

from typing import Any, List, Tuple, Type
from .constants import *
from . import lib

INTERPS = {
    I_CONST: "constant",
    I_LIN: "linear",
    I_SINE: "sine",
}


class Keyframe:
    frame: float
    value: Any
    interp: int

    def __init__(self, frame: float, value: Any, interp: int):
        self.frame = frame
        self.value = value
        self.interp = interp


class Property:
    type: Type
    default: Any
    supported_interps: Tuple[int]
    keyframes: List[Keyframe]

    def __init__(self, default: Any) -> None:
        self.keyframes = []
        self.default = default

    def key(self, frame: float, value: Any, interp: int) -> None:
        """
        Add a keyframe.
        """
        if self.supported_interps != "ALL":
            assert (interp in self.supported_interps), "Interpolation not supported."
        self.keyframes.append(Keyframe(frame, value, interp))

    def value(self, frame: float) -> Any:
        """
        Get value at frame, depending on keyframes.
        If no keyframes are present, the default is returned.
        """
        return interpolate(self.keyframes, frame, self.default)

class VectorProp:
    type: Type[Property]
    length: int
    props: List[Property]
    defaults: Tuple[Any, ...]

    def __init__(self, type: Type[Property], length: int, defaults: Tuple[Any, ...]) -> None:
        self.type = type
        self.length = length
        self.props = [type(defaults[i]) for i in range(length)]
        self.defaults = defaults

    def __getitem__(self, idx: int) -> Property:
        return self.props[idx]

    def key(self, frame: float, values: Tuple[Any, ...], interp: int) -> None:
        for i in range(self.length):
            self.props[i].key(frame, values[i], interp)

    def value(self, frame: float) -> List[Any]:
        return [self.props[i].value(frame) for i in range(self.length)]

class BoolProp(Property):
    type = bool
    supported_interps = (I_CONST,)

class IntProp(Property):
    type = int
    supported_interps = "ALL"

class FloatProp(Property):
    type = float
    supported_interps = "ALL"

class StrProp(Property):
    type = str
    supported_interps = (I_CONST,)


def interpolate(keyframes: List[Keyframe], frame: float, default: Any) -> Any:
    if len(keyframes) == 0:
        return default

    elif len(keyframes) == 1:
        return keyframes[0].value

    else:
        if frame <= keyframes[0].frame:
            return keyframes[0].value
        elif frame >= keyframes[-1].frame:
            return keyframes[-1].value
        else:
            ind = 0
            for i in range(len(keyframes)):
                if keyframes[i].frame == frame:
                    return keyframes[i].value
                if keyframes[i].frame > frame:
                    ind = i - 1
                    break

            f1 = keyframes[ind].frame
            f2 = keyframes[ind+1].frame
            v1 = keyframes[ind].value
            v2 = keyframes[ind+1].value

            func = INTERPS[keyframes[ind].interp]
            return getattr(lib.interp, func)(f1, f2, v1, v2, frame)
