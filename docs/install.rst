Installation
============

You can install from PyPI with Pip:

``pip install csanim``

After installing, you need to compile the C++ libraries.
CS Anim will ask you interactively on import. Simply
import the module:

.. code-block:: python

    >>> import csanim
    csanim: libdraw.so missing
    csanim: libinterp.so missing
    csanim: some libraries missing.
    csanim: compile libraries? [y/N] y
    csanim: running "make" in /home/patrick/.virtualenvs/general/lib/python3.8/site-packages/csanim
    /usr/bin/g++ -Wall -O3 -c -fPIC draw.cpp interp.cpp
    /usr/bin/g++ -shared -o libdraw.so draw.o
    /usr/bin/g++ -shared -o libinterp.so interp.o
    rm *.o
    csanim: compilation successful

Building the libraries requires ``g++`` and ``make``.
