from sage.all import var
from r_solver_utils.element import Element, RES_TYPE, VOLTAGE_TYPE, VCVS_TYPE

def parse_netlist(file):
    lines = file.readlines()

    num_nodes = 0
    num_voltages = 0
    num_resistors = 0
    num_extras = 0
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
        elif l[0] == 'E':
            el_type = VCVS_TYPE
            num_extras += 1
        
        parts = l.split(' ')
        el_impedance = parts[0]
        el_node1 = int(parts[1])
        el_node2 = int(parts[2])

        num_nodes = max(num_nodes, el_node1, el_node2)

        if el_type == VCVS_TYPE:
            el_node3 = int(parts[3])
            el_node4 = int(parts[4])
            el_gain = var(parts[5])
            elements.append(Element(type=el_type, node1=el_node1 - 1, node2=el_node2 - 1,
                            impedance=var(el_impedance), port=num_extras - 1, node3=el_node3 -1,
                            node4=el_node4 - 1, gain=el_gain))
        else:
            elements.append(Element(type=el_type, node1=el_node1 - 1, node2=el_node2 - 1,
                            impedance=var(el_impedance), port=port))
        
    assert(num_resistors == num_voltages)
    num_ports = num_voltages

    return elements, num_nodes, num_ports, num_extras
