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
#include <cmath>

using std::min;
using std::max;

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


void mix(UCH* dest, const UCH* c1, const UCH* c2, const double fac) {
    for (int i = 0; i < 3; i++)
        dest[i] = c1[i]*(1-fac) + c2[i]*fac;
}

double pythag(const double dx, const double dy) {
    return std::pow((dx*dx) + (dy*dy), 0.5);
}

int ibounds(const int v, const int vmin = 0, const int vmax = 1) {
    return min(max(v, vmin), vmax);
}

double dbounds(const double v, const double vmin = 0, const double vmax = 1) {
    return min(max(v, vmin), vmax);
}


extern "C" void circle(UCH* img, const UINT width, const UINT height, const double cx, const double cy,
        const double rad, const double border, const double r, const double g, const double b, const double a) {
    const int xmin = max((int)(cx-rad-1), 0);
    const int xmax = min((int)(cx+rad+1), (int)width-1);
    const int ymin = max((int)(cy-rad-1), 0);
    const int ymax = min((int)(cy+rad+1), (int)height-1);

    const double afac = a / 255;
    const double out_thres = rad;
    const double in_thres = (border == 0 ? 0 : (rad-border));
    const UCH c1[3] = {(UCH)r, (UCH)g, (UCH)b};

    for (int x = xmin; x <= xmax; x++) {
        for (int y = ymin; y <= ymax; y++) {
            const double dist = pythag(x-cx, y-cy);
            const double out_fac = dbounds(out_thres-dist+1);
            const double in_fac = dbounds(dist-in_thres+1);

            UCH c2[3], color[3];
            getc(img, width, x, y, c2);
            mix(color, c2, c1, out_fac*in_fac*afac);
            setc(img, width, x, y, color[0], color[1], color[2]);
        }
    }
}
