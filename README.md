# R-Solver

A Python tools for deriving R-Type adaptors for
[Wave Digital Filters](https://github.com/jatinchowdhury18/WaveDigitalFilters).

This code is not quite production-ready. If you are
interested in contributing, please contact me through
this repository.

## How It Works

In order to use this script, you must have the
[Sage](https://www.sagemath.org/) software system
installed. From there, you can run the `r_solver.py`
script using the command
`/usr/bin/env sage -python r_solver.py my_netlist.txt`,
to generate a scattering matrix for a given
netlist. For more options, use `r_solver.py --help`.

## Netlist Format
The format for the input netlists can be seen in the
example netlists provided in the `netlists/` directory.
One important thing to note, is that all resistors must
be given a 2-character label, e.g. 'Ra'.
