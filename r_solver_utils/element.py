from collections import namedtuple

Element = namedtuple('Element', ['type', 'node1', 'node2', 'impedance', 'port'])

RES_TYPE = 'Res'
VOLTAGE_TYPE = 'Vs'
