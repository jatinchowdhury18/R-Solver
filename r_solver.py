# Simple script for generating R-type adaptors.
# The resulting Scattring matrics will be in terms
# of both port impedance (Rp) and admittance (Gp = 1/Rp)
#
# There's still a lot of work to do with this script, starting with:
# - Allow one port to be adapted
# - Add support for VCVS and Resistive VCVS elements

import argparse
from r_solver_utils.parse_netlist import parse_netlist
from r_solver_utils.matrix_helpers import compute_S_matrix, construct_X_matrix, remove_datum_node
from r_solver_utils.print_helpers import print_matrix, print_shape

def main(args):
    elements, num_nodes, num_ports = parse_netlist(args.netlist)
    
    X_mat = construct_X_matrix(elements, num_nodes, num_ports)
    if args.verbose:
        print('Original X matrix:')
        print(X_mat)
        print_shape(X_mat)

    X_mat = remove_datum_node(X_mat, int(args.datum))
    if args.verbose:
        print('')
        print('X matrix after removing datum node:')
        print(X_mat)
        print_shape(X_mat)

    X_inv = X_mat.inverse().simplify_rational()
    if args.verbose:
        print('')
        print('X matrix inverse:')
        print(X_inv)
        print_shape(X_inv)

    Scattering_mat = compute_S_matrix(X_inv, elements, num_ports)

    print('')
    print('Scattering matrix:')
    print_matrix(Scattering_mat, args.out_file, num_ports)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Derive the R-type scattering matrix for a given circuit.')
    
    parser.add_argument('netlist', type=argparse.FileType('r'),
                        help='The netlist to construct the matrix for')

    parser.add_argument('--datum', dest='datum', default=0,
                        help='The \"datum\" node to remove from the MNA matrix')

    parser.add_argument('--out', dest='out_file', type=argparse.FileType('w'), default=None,
                        help='Output file to write the scattering matrix to')

    parser.add_argument('--verbose', action='store_const', const=True,
                        help='Use this flag to have the solver print extra intermediate information')
    parser.set_defaults(verbose=False)

    args = parser.parse_args()
    main(args)
