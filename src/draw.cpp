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
Functions for drawing antialiased shapes.
Takes in a numpy array as an image with shape (height, width, 3)
img variables are raveled numpy arrays.
*/

#include <iostream>
#include <cmath>

using std::min;
using std::max;

typedef  unsigned char  UCH;
typedef  unsigned int   UINT;
typedef  const double   CD;


void set(UCH* img, const UINT width, const UINT x, const UINT y, const UCH channel, const UCH value) {
    /*
    Sets pixel and channel of image to a value.

    :param img: Image.
    :param width: Image width.
    :param x: X coordinate.
    :param y: Y coordinate.
    :param channel: Channel number, corresponding to B, G, R.
    :param value: Number from 0 to 255.
    */
    img[3*(y*width + x) + channel] = value;
}

void setc(UCH* img, const UINT width, const UINT x, const UINT y, const UCH r, const UCH g, const UCH b) {
    /*
    Sets pixel to color. Equivalent to three calls of set()

    :param img: Image.
    :param width: Image width.
    :param x: X coordinate.
    :param y: Y coordinate.
    :param r, g, b: R, G, B values.
    */
    set(img, width, x, y, 0, r);
    set(img, width, x, y, 1, g);
    set(img, width, x, y, 2, b);
}

void get(UCH* img, const UINT width, const UINT x, const UINT y, const UCH channel, UCH* value) {
    /*
    Gets value at pixel and channel and modifies "value" param.

    :param img: Image.
    :param width: Image width.
    :param x: X coordinate.
    :param y: Y coordinate.
    :param channel: Channel number, corresponding to B, G, R.
    :param value: Value pointer. Will be modified to be the obtained value.
    */
    value[0] = img[3*(y*width + x) + channel];
}

void getc(UCH* img, const UINT width, const UINT x, const UINT y, UCH* color) {
    /*
    Gets value at pixel and modifies "value" param. Equivalent to 3 calls of get()

    :param img: Image.
    :param width: Image width.
    :param x: X coordinate.
    :param y: Y coordinate.
    :param value: Value pointer. Will be modified to be the obtained value.
    */
    get(img, width, x, y, 0, color+0);
    get(img, width, x, y, 1, color+1);
    get(img, width, x, y, 2, color+2);
}


void mix(UCH* dest, const UCH* c1, const UCH* c2, CD fac) {
    /*
    Mixes two colors with a factor.

    :param dest: Destination array. Will be modified.
    :param c1: Color 1.
    :param c2: Color 2.
    :param fac: Factor. 0 = full c1, 1 = full c2
    */
    for (int i = 0; i < 3; i++)
        dest[i] = c1[i]*(1-fac) + c2[i]*fac;
}

double pythag(CD dx, CD dy) {
    /*
    Pythagorean distance.

    :param dx: X delta.
    :param dy: Y delta.
    */
    return std::pow((dx*dx) + (dy*dy), 0.5);
}

int ibounds(const int v, const int vmin = 0, const int vmax = 1) {
    /*
    Integer bounds.

    :param v: Value.
    :param vmin: Minimum value.
    :param vmax: Maximum value.
    */
    return min(max(v, vmin), vmax);
}

double dbounds(CD v, CD vmin = 0, CD vmax = 1) {
    /*
    Double bounds.

    :param v: Value.
    :param vmin: Minimum value.
    :param vmax: Maximum value.
    */
    return min(max(v, vmin), vmax);
}


extern "C" void circle(UCH* img, const UINT width, const UINT height, CD cx, CD cy,
        CD rad, CD border, CD r, CD g, CD b, CD a) {
    /*
    Draws a circle.

    :param img: Image.
    :param width: Image width.
    :param height: Image height.
    :param cx: Center X.
    :param cy: Center Y.
    :param rad: Radius.
    :param border: Border thickness. Set to 0 for filled.
    :param r, g, b, a: R, G, B, A values.
    */
    const int xmin = max((int)(cx-rad-1), 0);
    const int xmax = min((int)(cx+rad+1), (int)width-1);
    const int ymin = max((int)(cy-rad-1), 0);
    const int ymax = min((int)(cy+rad+1), (int)height-1);

    CD afac = a / 255;
    CD out_thres = rad;
    CD in_thres = (border == 0 ? 0 : (rad-border));
    const UCH c1[3] = {(UCH)r, (UCH)g, (UCH)b};

    for (int x = xmin; x <= xmax; x++) {
        for (int y = ymin; y <= ymax; y++) {
            CD dist = pythag(x-cx, y-cy);
            CD out_fac = dbounds(out_thres-dist+1);
            CD in_fac = dbounds(dist-in_thres+1);

            UCH c2[3], color[3];
            getc(img, width, x, y, c2);
            mix(color, c2, c1, out_fac*in_fac*afac);
            setc(img, width, x, y, color[0], color[1], color[2]);
        }
    }
}

extern "C" void rect(UCH* img, const UINT width, const UINT height, CD dx, CD dy, CD dw, CD dh,
        CD border, CD border_rad, CD tl_rad, CD tr_rad, CD bl_rad, CD br_rad, CD r, CD g, CD b, CD a) {
    /*
    Draws a rectangle.

    :param img: Image.
    :param width: Image width.
    :param height: Image height.
    :param dx: Top left X.
    :param dy: Top left Y.
    :param dw: Width.
    :param dh: Height.
    :param border: Border thickness. Set to 0 for filled.
    :param border_rad: Radius of corner rounding.
    :param tl_rad: Top left corner radius.
    :param tr_rad: Top right corner radius.
    :param bl_rad: Bottom left corner radius.
    :param br_rad: Bottom right corner radius.
    */
    CD radii[4] = {
        (tl_rad < 0) ? border_rad : tl_rad,
        (tr_rad < 0) ? border_rad : tr_rad,
        (br_rad < 0) ? border_rad : br_rad,
        (bl_rad < 0) ? border_rad : bl_rad,
    };
    double thresholds[4];
    for (int i = 0; i < 4; i++)
        thresholds[i] = ((border == 0) ? 0 : (radii[i]-border));

    CD afac = a / 255;
    const UCH c1[3] = {(UCH)r, (UCH)g, (UCH)b};

    const int xmin = max((int)(dx-1), 0);
    const int xmax = min((int)(dx+dw+1), (int)width);
    const int ymin = max((int)(dy-1), 0);
    const int ymax = min((int)(dy+dh+1), (int)height);
    for (int x = xmin; x <= xmax; x++) {
        for (int y = ymin; y <= ymax; y++) {
            bool is_corner = false;
            UCH corner_no;
            double corner_pos[2];
            if (x < dx+radii[0] && y < dy+radii[0]) {
                is_corner = true;
                corner_no = 0;
                corner_pos[0] = dx+radii[0];
                corner_pos[1] = dy+radii[0];
            } else if (x > dx+dw-radii[1] && y < dy+radii[1]) {
                is_corner = true;
                corner_no = 1;
                corner_pos[0] = dx+dw-radii[1];
                corner_pos[1] = dy+radii[1];
            } else if (x > dx+dw-radii[2] && y > dy+dh-radii[2]) {
                is_corner = true;
                corner_no = 2;
                corner_pos[0] = dx+dw-radii[2];
                corner_pos[1] = dy+dh-radii[2];
            } else if (x < dx+radii[3] && y > dy+dh-radii[3]) {
                is_corner = true;
                corner_no = 3;
                corner_pos[0] = dx+radii[3];
                corner_pos[1] = dy+dh-radii[3];
            }

            double final_fac;
            if (is_corner) {
                CD dist = pythag(x-corner_pos[0], y-corner_pos[1]);
                CD out_fac = dbounds(radii[corner_no]-dist+1);
                CD in_fac = dbounds(dist-thresholds[corner_no]+1);
                final_fac = out_fac*in_fac*afac;
            } else {
                CD out_fac = dbounds(x-dx+1) * dbounds(dx+dw-x+1) * dbounds(y-dy+1) * dbounds(dy+dh-y+1);
                CD in_fac = (border == 0) ? 1 :
                    dbounds(dx+border-x+1) + dbounds(x-(dx+dw-border)+1) + dbounds(dy+border-y+1) + dbounds(y-(dy+dh-border)+1);
                final_fac = out_fac*in_fac*afac;
            }

            UCH c2[3], color[3];
            getc(img, width, x, y, c2);
            mix(color, c2, c1, final_fac);
            setc(img, width, x, y, color[0], color[1], color[2]);
        }
    }
}
