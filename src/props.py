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
    "Property",
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
    """
    A keyframe class which contains three values:
    * frame: The frame.
    * value: The value. Can be any type.
    * interp: The interpolation of this keyframe and the next.
    """
    frame: float
    value: Any
    interp: int

    def __init__(self, frame: float, value: Any, interp: int):
        """
        Initializes keyframe.
        """
        self.frame = frame
        self.value = value
        self.interp = interp


class Property:
    """
    Base property class. All other props extend from this.

    Inherit and define:
    * type: The property type.
    * supported_interps: Supported interpolations. "ALL" = all supported.
    * default_interp: Default interpolation to use.
    """
    type: Type
    supported_interps: Tuple[int]
    default_interp: int

    default: Any
    keyframes: List[Keyframe]

    def __init__(self, default: Any) -> None:
        """
        Initializes the property.
        :param default: The default value (returned if no keyframes are present).
        """
        self.keyframes = []
        self.default = default

    def key(self, frame: float, value: Any, interp: int = None) -> None:
        """
        Add a keyframe.
        """
        if interp is None:
            interp = self.default_interp
        if self.supported_interps != "ALL":
            assert (interp in self.supported_interps), "Interpolation not supported."
        self.keyframes.append(Keyframe(frame, value, interp))

    def value(self, frame: float) -> Any:
        """
        Get value at frame, depending on keyframes.
        If no keyframes are present, the default is returned.
        """
        return _interpolate(self.keyframes, frame, self.default)

class VectorProp:
    """
    A static sized list of props of the same type.
    """
    type: Type[Property]
    length: int
    props: List[Property]
    defaults: Tuple[Any, ...]

    def __init__(self, type: Type[Property], length: int, defaults: Tuple[Any, ...]) -> None:
        """
        Initializes the property.
        :param type: The prop type. e.g. BoolProp, IntProp, ...
        :param length: Vector length.
        :param defaults: Default values of all the props. len(defaults) == length
        """
        assert length >= 0
        assert len(defaults) == length
        self.type = type
        self.length = length
        self.props = [type(defaults[i]) for i in range(length)]
        self.defaults = defaults

    def __getitem__(self, idx: int) -> Property:
        """
        Gets nth property.
        """
        return self.props[idx]

    def key(self, frame: float, values: List[Any], interp: int = None) -> None:
        """
        Adds keyframe to all props.
        To add a keyframe to one prop, do vecprop[i].key()
        :param frame: Frame.
        :param values: Values. len(values) == length
        :param interp: Interpolation for all the props.
        """
        assert len(values) == self.length
        if interp is None:
            interp = self.type.default_interp
        for i in range(self.length):
            self.props[i].key(frame, values[i], interp)

    def value(self, frame: float) -> List[Any]:
        """
        Returns list of all values at frame.
        """
        return [self.props[i].value(frame) for i in range(self.length)]

class BoolProp(Property):
    """
    Boolean property.
    """
    type = bool
    supported_interps = (I_CONST,)
    default_interp = I_CONST

class IntProp(Property):
    """
    Integer property (unbounded).
    """
    type = int
    supported_interps = "ALL"
    default_interp = I_SINE

class FloatProp(Property):
    """
    Float property (64 bit).
    """
    type = float
    supported_interps = "ALL"
    default_interp = I_SINE

class StrProp(Property):
    """
    String property.
    """
    type = str
    supported_interps = (I_CONST,)
    default_interp = I_CONST


def _closest_ind(keyframes: List[Keyframe], frame: float) -> int:
    """
    Internal function.
    Binary search for the closest index.
    """
    imin = 0
    imax = len(keyframes) - 1

    while True:
        if imax-imin == 1:
            if keyframes[imax].frame <= frame:
                return imax
            return imin

        mid = (imax+imin) // 2
        if keyframes[mid].frame > frame:
            imax = mid
        else:
            imin = mid


def _interpolate(keyframes: List[Keyframe], frame: float, default: Any) -> Any:
    """
    Internal function.
    Finds value at frame, given keyframes.
    """
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
            ind = _closest_ind(keyframes, frame)
            f1 = keyframes[ind].frame
            f2 = keyframes[ind+1].frame
            v1 = keyframes[ind].value
            v2 = keyframes[ind+1].value

            func = INTERPS[keyframes[ind].interp]
            return getattr(lib.interp, func)(f1, f2, v1, v2, frame)
