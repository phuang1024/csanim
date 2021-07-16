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

#define  PI  3.1415926535

#include <cmath>

typedef  const double  CD;


extern "C" double linear(CD f1, CD f2, CD v1, CD v2, CD frame) {
    CD fac = (frame-f1) / (f2-f1);
    return v1 + (v2-v1)*fac;
}

extern "C" double sine(CD f1, CD f2, CD v1, CD v2, CD frame) {
    CD fac = (frame-f1) / (f2-f1);
    CD new_fac = std::sin((PI*fac)-(PI/2));
    return v1 + (v2-v1)*new_fac;
}
