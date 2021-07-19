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
A library for creating computer science explanatory videos.
Official GitHub: https://github.com/phuang1024/csanim
"""

import os
import subprocess

PARENT = os.path.dirname(os.path.realpath(__file__))
REQUIRED_LIBS = (
    "libdraw.so",
    "libinterp.so",
)


def check_libs():
    """
    Checks that all required Shared Object files are present.
    If some are missing, the user will be prompted from stdin
    to compile them.
    """
    missing = False
    for lib in REQUIRED_LIBS:
        path = os.path.join(PARENT, lib)
        if not os.path.isfile(path):
            print(f"csanim: {lib} missing")
            missing = True
        else:
            with open(path, "rb") as file:
                if len(file.read(10)) < 10:
                    print(f"csanim: {lib} missing")
                    missing = True

    if missing:
        print("csanim: some libraries missing.")
        if "CSANIM_NO_COMPILE" in os.environ:
            print("csanim: not compiling because CSANIM_NO_COMPILE env variable is present")
            return False
        else:
            if input("csanim: compile libraries? [y/N] ").lower().strip() == "y":
                print(f"csanim: running \"make\" in {PARENT}")
                p = subprocess.Popen(["make"], cwd=PARENT)
                p.wait()
                if p.returncode == 0:
                    print(f"csanim: compilation successful")
                    return True
                else:
                    print(f"csanim: compilation failed")
                    return False
            else:
                return False

    return True


if check_libs():
    from .constants import *
    from .elements import *
    from . import props
    from .scene import *
    from .video import Video
else:
    print("csanim: module empty because libraries missing")
