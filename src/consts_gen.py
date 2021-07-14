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
Generates constants.py
"""

import os

PARENT = os.path.dirname(os.path.realpath(__file__))
FILE = os.path.join(PARENT, "constants.py")
CONSTS = [
    "TR_CUT",
    "TR_FADE",
    "TR_FADEIO",
]


def main():
    with open(os.path.realpath(__file__), "r") as file:
        gpl = "".join([file.readline() for _ in range(18)])

    with open(FILE, "w") as file:
        file.write(gpl)
        file.write("\n")

        file.write("__all__ = [\n")
        for const in CONSTS:
            file.write(f"    \"{const}\",\n")
        file.write("]\n\n")

        for i, const in enumerate(CONSTS):
            file.write(f"{const}: int = {i}\n")


main()
