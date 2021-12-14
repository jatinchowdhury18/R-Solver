# Simple script for generating R-type adaptors.
# The resulting Scattring matrics will be in terms
# of the port impedance (Rp).
#
# There's still a lot of work to do with this script, starting
# with adding support for VCVS and Resistive VCVS elements

import argparse
from r_solver_utils.parse_netlist import parse_netlist
from r_solver_utils.matrix_helpers import adapt_port, compute_S_matrix, construct_X_matrix, remove_datum_node
from r_solver_utils.print_helpers import print_matrix, print_shape, verbose_print

def main(args):
    elements, num_nodes, num_ports = parse_netlist(args.netlist)
    
    X_mat = construct_X_matrix(elements, num_nodes, num_ports)
    if args.verbose:
        verbose_print(X_mat, 'Original X matrix:')

    X_mat = remove_datum_node(X_mat, int(args.datum))
    if args.verbose:
        verbose_print(X_mat, 'X matrix after removing datum node:')

    X_inv = X_mat.inverse().simplify_rational() # simplify_rational() is faster than simplify_full(), and seems to give the same answer!
    if args.verbose:
        verbose_print(X_inv, 'X matrix inverse:')

    Scattering_mat, Rp = compute_S_matrix(X_inv, elements, num_ports)

    port_to_adapt = int(args.adapted_port)
    if port_to_adapt <= 0:
        Scattering_mat = adapt_port(Scattering_mat, Rp, port_to_adapt)

    print('')
    print('Scattering matrix:')
    print_matrix(Scattering_mat, args.out_file, num_ports)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Derive the R-type scattering matrix for a given circuit.')
    
    parser.add_argument('netlist', type=argparse.FileType('r'),
                        help='The netlist to construct the matrix for')

    parser.add_argument('--datum', dest='datum', default=0,
                        help='The \"datum\" node to remove from the MNA matrix')

    parser.add_argument('--adapt', dest='adapted_port', default=-1,
                        help='Specify a port index to adapt. If this argument is not specified, no port will be adapted. Note that indexing starts at 0.')

    parser.add_argument('--out', dest='out_file', type=argparse.FileType('w'), default=None,
                        help='Output file to write the scattering matrix to')

    parser.add_argument('--verbose', action='store_const', const=True,
                        help='Use this flag to have the solver print extra intermediate information')
    parser.set_defaults(verbose=False)

    args = parser.parse_args()
    main(args)
