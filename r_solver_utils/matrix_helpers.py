from sage.all import matrix, SR, identity_matrix, solve

from r_solver_utils.element_stamps import stamp_element
from r_solver_utils.element_stamps import RES_TYPE


def construct_X_matrix(elements, num_nodes, num_ports):
    '''Constructs an \'X\' Matrix for doing MNA'''
    X_mat = matrix(SR, num_nodes + num_ports, num_nodes + num_ports)

    for el in elements:
        X_mat = stamp_element(X_mat, el, num_nodes, num_ports)
    
    return X_mat


def remove_datum_node(X_mat, datum):
    matrix_range = [x for x in range(X_mat.nrows()) if x != datum]
    return matrix(X_mat[matrix_range, matrix_range])


def compute_S_matrix(X_inv, elements, num_ports):
    vert_id = matrix(SR, X_inv.nrows(), num_ports)
    vert_id[-num_ports:, :] = identity_matrix(num_ports)

    hor_id = matrix(SR, num_ports, X_inv.ncols())
    hor_id[:, -num_ports:] = identity_matrix(num_ports)

    Rp_diag = matrix(SR, num_ports, num_ports)
    for el in elements:
        if el.type == RES_TYPE:
            Rp_diag[el.port, el.port] = el.impedance

    S_mat = identity_matrix(num_ports) + 2 * Rp_diag * hor_id * X_inv * vert_id
    return S_mat, Rp_diag


def adapt_port(S_mat, Rp, port):
    '''Adapts one port of the scattering matrix to be a reflection-free port'''
    if port < 0 or port >= S_mat.nrows():
        raise IndexError('Port index must be less than the number of available ports')

    S_nn = S_mat[port, port]
    R_n = Rp[port, port]
    R_n_solved = solve(S_nn == 0, R_n)[0].right()

    return S_mat.substitute({R_n: R_n_solved}).simplify_full()
