from collections import namedtuple, Mapping

def namedtuple_with_defaults(typename, field_names, default_values=()):
    T = namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(default_values, Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T

fields = ('type', 'node1', 'node2', 'impedance', 'port', 'node3', 'node4', 'gain')
Element = namedtuple_with_defaults('Element', fields, (None,) * len(fields))

RES_TYPE = 'Res'
VOLTAGE_TYPE = 'Vs'
VCVS_TYPE = 'VCVS'
