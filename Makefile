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

CXX = /usr/bin/g++
PY = /usr/bin/python3

CXX_FLAGS = -Wall -O3 -c -fPIC
WHEEL_FLAGS = bdist_wheel sdist

CXX_FILES = draw.cpp

cpp:
	cd ./src; \
	$(CXX) $(CXX_FLAGS) $(CXX_FILES); \
	$(CXX) -shared -o libdraw.so draw.o; \
	rm *.o;

wheel:
	cd ./build; \
	$(PY) ./setup.py $(WHEEL_FLAGS);

upload:
	cd ./build; \
	twine upload ./dist/*;
