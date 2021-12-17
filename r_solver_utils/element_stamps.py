from sage.all import var
from r_solver_utils.element import RES_TYPE, VOLTAGE_TYPE, VCVS_TYPE

def stamp_resistor(X_matrix, resistor):
    X_matrix[resistor.node1, resistor.node1] += 1 / resistor.impedance
    X_matrix[resistor.node2, resistor.node2] += 1 / resistor.impedance
    X_matrix[resistor.node1, resistor.node2] -= 1 / resistor.impedance
    X_matrix[resistor.node2, resistor.node1] -= 1 / resistor.impedance

    return X_matrix


def stamp_voltage(X_matrix, voltage, num_nodes):
    X_matrix[num_nodes + voltage.port, voltage.node1] += 1
    X_matrix[num_nodes + voltage.port, voltage.node2] += -1

    X_matrix[voltage.node1, num_nodes + voltage.port] += 1
    X_matrix[voltage.node2, num_nodes + voltage.port] += -1

    return X_matrix


def stamp_vcvs(X_matrix, vcvs, num_nodes, num_ports):
    R_in = var('Ri')
    R_out = var('Ro')
    extra_idx = num_nodes + num_ports

    X_matrix[extra_idx + vcvs.port, vcvs.node1] += -vcvs.gain
    X_matrix[extra_idx + vcvs.port, vcvs.node2] += vcvs.gain
    
    X_matrix[extra_idx + vcvs.port, vcvs.node3] += 1
    X_matrix[extra_idx + vcvs.port, vcvs.node4] += -1

    X_matrix[vcvs.node3, extra_idx + vcvs.port] += 1
    X_matrix[vcvs.node4, extra_idx + vcvs.port] += -1

    X_matrix[vcvs.node1, vcvs.node1] += 1 / R_in
    X_matrix[vcvs.node2, vcvs.node2] += 1 / R_in
    X_matrix[vcvs.node1, vcvs.node2] -= 1 / R_in
    X_matrix[vcvs.node2, vcvs.node1] -= 1 / R_in

    X_matrix[extra_idx + vcvs.port, extra_idx + vcvs.port] += R_out

    return X_matrix


def stamp_element(X_matrix, element, num_nodes, num_ports):
    if element.type == RES_TYPE:
        X_matrix = stamp_resistor(X_matrix, element)
    elif element.type == VOLTAGE_TYPE:
        X_matrix = stamp_voltage(X_matrix, element, num_nodes)
    elif element.type == VCVS_TYPE:
        X_matrix = stamp_vcvs(X_matrix, element, num_nodes, num_ports)
    
    return X_matrix
