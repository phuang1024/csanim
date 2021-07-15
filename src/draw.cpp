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

#include <iostream>

typedef  unsigned char  UCH;
typedef  unsigned int   UINT;


void set(UCH* img, const UINT width, const UINT x, const UINT y, const UCH channel, const UCH value) {
    img[3*(y*width + x) + channel] = value;
}

void setc(UCH* img, const UINT width, const UINT x, const UINT y, const UCH r, const UCH g, const UCH b) {
    set(img, width, x, y, 0, r);
    set(img, width, x, y, 1, g);
    set(img, width, x, y, 2, b);
}

void get(UCH* img, const UINT width, const UINT x, const UINT y, const UCH channel, UCH* value) {
    value[0] = img[3*(y*width + x) + channel];
}

void getc(UCH* img, const UINT width, const UINT x, const UINT y, UCH* color) {
    get(img, width, x, y, 0, color+0);
    get(img, width, x, y, 1, color+1);
    get(img, width, x, y, 2, color+2);
}


extern "C" void circle(UCH* img, const UINT width, const UINT height) {
    setc(img, width, 5, 5, 255, 255, 255);
}
