from r_solver_utils.element import RES_TYPE, VOLTAGE_TYPE

def stamp_resistor(X_matrix, resistor):
    X_matrix[resistor.node1, resistor.node1] += 1 / resistor.impedance
    X_matrix[resistor.node2, resistor.node2] += 1 / resistor.impedance
    X_matrix[resistor.node1, resistor.node2] -= 1 / resistor.impedance
    X_matrix[resistor.node2, resistor.node1] -= 1 / resistor.impedance

    return X_matrix

def stamp_voltage(X_matrix, voltage, num_nodes):
    X_matrix[num_nodes + voltage.port, voltage.node1] = 1
    X_matrix[num_nodes + voltage.port, voltage.node2] = -1

    X_matrix[voltage.node1, num_nodes + voltage.port] = 1
    X_matrix[voltage.node2, num_nodes + voltage.port] = -1

    return X_matrix

def stamp_element(X_matrix, element, num_nodes, num_ports):
    if element.type == RES_TYPE:
        X_matrix = stamp_resistor(X_matrix, element)
    elif element.type == VOLTAGE_TYPE:
        X_matrix = stamp_voltage(X_matrix, element, num_nodes)
    
    return X_matrix
