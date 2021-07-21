//
//  CS Animation
//  A tool for creating computer science explanatory videos.
//  Copyright Patrick Huang 2021
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//

/*
Interpolation between two keyframes.
*/

#define  PI  3.1415926535

#include <iostream>
#include <cmath>

typedef  const double  CD;


double range(CD old_min, CD old_max, CD new_min, CD new_max, CD value) {
    /*
    Maps a value from an old range to a new range.

    :param old_min: Old minimum.
    :param old_max: Old maximum.
    :param new_min: New minimum.
    :param new_max: New maximum.
    :param value: Value to map.
    */
    CD fac = (value-old_min) / (old_max-old_min);
    CD new_v = fac*(new_max-new_min) + new_min;
    return new_v;
}


double sin(CD x_min, CD x_max, CD y_min, CD y_max, CD fac) {
    /*
    A easier-to-use sine function.

    :param x_min: X minimum.
    :param x_max: X maximum.
    :param y_min: Output minimum.
    :param y_max: Output maximum.
    :param fac: Input factor. Mapped to x_min, x_max.
    */
    CD fac_x = fmod(x_min + fac*(x_max-x_min), 1.);
    CD real_x = range(0, 1, 0, PI*2, fac_x);
    CD output = std::sin(real_x);
    CD out_y = range(-1, 1, y_min, y_max, output);
    return out_y;
}


extern "C" double linear(CD f1, CD f2, CD v1, CD v2, CD frame) {
    /*
    Linear interpolation between two keyframes.
    */
    CD fac = (frame-f1) / (f2-f1);
    return v1 + (v2-v1)*fac;
}

extern "C" double sine(CD f1, CD f2, CD v1, CD v2, CD frame) {
    /*
    Sine interpolation between two keyframes.
    Uses the section with non-negative derivative.
    */
    CD fac = (frame-f1) / (f2-f1);
    return sin(-0.25, 0.25, v1, v2, fac);
}
