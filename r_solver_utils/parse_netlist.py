from r_solver_utils.element import VOLTAGE_TYPE
from sage.all import var
from r_solver_utils.element import Element, RES_TYPE, VOLTAGE_TYPE

def parse_netlist(file):
    lines = file.readlines()

    num_nodes = 0
    num_voltages = 0
    num_resistors = 0
    elements = []
    for l in lines:
        if l[0] == 'R':
            el_type = RES_TYPE
            port = num_resistors
            num_resistors += 1
        elif l[0] == 'V':
            el_type = VOLTAGE_TYPE
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
