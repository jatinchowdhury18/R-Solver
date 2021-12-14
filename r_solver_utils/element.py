from collections import namedtuple

Element = namedtuple('Element', ['type', 'node1', 'node2', 'impedance', 'admittance', 'port'])

RES_TYPE = 'Res'
VOLTAGE_TYPE = 'Vs'
