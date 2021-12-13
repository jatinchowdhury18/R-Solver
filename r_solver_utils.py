from sage.all import *
from collections import namedtuple

Element = namedtuple('Element', ['type', 'node1', 'node2', 'impedance', 'admittance', 'port'])

def parse_netlist(file):
    lines = file.readlines()

    num_nodes = 0
    num_voltages = 0
    num_resistors = 0
    elements = []
    for l in lines:
        if l[0] == 'R':
            el_type = 'Res'
            port = num_resistors
            num_resistors += 1
        elif l[0] == 'V':
            el_type = 'Vs'
            port = num_voltages
            num_voltages += 1
        
        parts = l.split(' ')
        el_impedance = parts[0]
        el_admittance = el_impedance.replace('R', 'G')
        
        el_node1 = int(parts[1])
        el_node2 = int(parts[2])

        num_nodes = max(num_nodes, el_node1, el_node2)

        elements.append(Element(type=el_type, node1=el_node1 - 1, node2=el_node2 - 1,
                        impedance=var(el_impedance), admittance=var(el_admittance), port=port))
        
    assert(num_resistors == num_voltages)
    num_ports = num_voltages

    return elements, num_nodes, num_ports

def stamp_resistor(X_matrix, resistor):
    X_matrix[resistor.node1, resistor.node1] += resistor.admittance
    X_matrix[resistor.node2, resistor.node2] += resistor.admittance
    X_matrix[resistor.node1, resistor.node2] -= resistor.admittance
    X_matrix[resistor.node2, resistor.node1] -= resistor.admittance

    return X_matrix

def print_matrix(M, out_file):
    M_strs = M.str(rep_mapping=lambda a: str(a) + ',')
    M_strs = M_strs.replace('[', '{').replace(',]', '},')
    M_strs = '{' + M_strs[:-1] + '};'
    print(M_strs)

    if out_file is not None:
        out_file.write(M_strs)

def shape(M):
    return (M.nrows(), M.ncols())

def stamp_voltage(X_matrix, voltage, num_nodes):
    X_matrix[num_nodes + voltage.port, voltage.node1] = 1
    X_matrix[num_nodes + voltage.port, voltage.node2] = -1

    X_matrix[voltage.node1, num_nodes + voltage.port] = 1
    X_matrix[voltage.node2, num_nodes + voltage.port] = -1

    return X_matrix

def stamp_element(X_matrix, element, num_nodes, num_ports):
    if element.type == 'Res':
        X_matrix = stamp_resistor(X_matrix, element)
    elif element.type == 'Vs':
        X_matrix = stamp_voltage(X_matrix, element, num_nodes)
    
    return X_matrix
