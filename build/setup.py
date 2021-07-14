#
#  Piano Video
#  Piano MIDI visualizer
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

import os
import shutil
import setuptools

PARENT = os.path.dirname(os.path.realpath(__file__))
DEST = os.path.join(PARENT, "csanim")
SRC = os.path.join(os.path.dirname(PARENT), "src")

with open("../README.md", "r") as file:
    long_description = file.read()

with open(os.path.join(os.path.dirname(PARENT), "requirements.txt"), "r") as file:
    requirements = file.read().strip().split("\n")

if os.path.isdir(DEST):
    if input(f"Destination {DEST} exists. Remove permanently? (y/N) ").lower().strip() == "y":
        shutil.rmtree(DEST)
    else:
        exit()
shutil.copytree(SRC, DEST)

setuptools.setup(
    name="csanim",
    version=os.path.basename(os.environ["PYPI_VERSION"]),
    author="Patrick Huang",
    author_email="huangpatrick16777216@gmail.com",
    description="A tool for creating computer science explanatory videos.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phuang1024/csanim",
    py_modules=["csanim"],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
)

shutil.rmtree(DEST)
