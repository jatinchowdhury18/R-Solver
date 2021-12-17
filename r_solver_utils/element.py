from collections import namedtuple

fields = ('type', 'node1', 'node2', 'impedance', 'port', 'node3', 'node4', 'gain')
Element = namedtuple('Element', fields, defaults=(None,) * len(fields))

RES_TYPE = 'Res'
VOLTAGE_TYPE = 'Vs'
VCVS_TYPE = 'VCVS'
