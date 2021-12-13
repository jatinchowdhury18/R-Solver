# Simple script for generating R-type adaptors.
# The resulting Scattring matrics will be in terms
# of both port impedance (Rp) and admittance (Gp = 1/Rp)
#
# There's still a lot of work to do with this script, starting with:
# - Allow one port to be adapted
# - Add support for VCVS and Resistive VCVS elements

from sage.all import *
import argparse
from r_solver_utils import stamp_element, parse_netlist, shape, print_matrix

def main(args):
    elements, num_nodes, num_ports = parse_netlist(args.netlist)

    X_mat = matrix(SR, num_nodes + num_ports, num_nodes + num_ports)

    for el in elements:
        X_mat = stamp_element(X_mat, el, num_nodes, num_ports)

    if args.verbose:
        print('Original X matrix:')
        print(X_mat)
        print(shape(X_mat))

    datum = int(args.datum)
    matrix_range = [x for x in range(num_nodes + num_ports) if x != datum]
    X_mat = matrix(X_mat[matrix_range, matrix_range])

    if args.verbose:
        print('')
        print('X matrix after removing datum node:')
        print(X_mat)
        print(shape(X_mat))

    X_inv = X_mat.inverse().simplify_rational()
    if args.verbose:
        print('')
        print('X matrix inverse:')
        print(X_inv)
        print(shape(X_inv))

    vert_id = matrix(SR, X_mat.nrows(), num_ports)
    vert_id[-num_ports:, :] = identity_matrix(num_ports)

    hor_id = matrix(SR, num_ports, X_mat.ncols())
    hor_id[:, -num_ports:] = identity_matrix(num_ports)

    Rp_diag = matrix(SR, num_ports, num_ports)
    for el in elements:
        if el.type == 'Res':
            Rp_diag[el.port, el.port] = el.impedance

    Scattering_mat = identity_matrix(num_ports) + 2 * Rp_diag * hor_id * X_inv * vert_id
    # Scattering_mat = Scattering_mat.simplify()

    print('')
    print('Scattering matrix:')
    print_matrix(Scattering_mat, args.out_file)

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
