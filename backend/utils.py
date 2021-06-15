import netifaces
import json
import copy


def get_interface_ipaddress(interface):
    info = netifaces.ifaddresses(interface)

    if 0 <= 2 < len(info):  # check if interface connected
        return info[2][0]['addr']
    else:  # interface not connected
        return 'offline'


def serialize(object, exclude=''):
    obj = copy.copy(object) # make a copy to prevent the pop function from removing the pwm instance and getting erros about it

    if exclude != '' and hasattr(obj, exclude):
        obj.__dict__.pop(exclude)

    data = json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True)

    return json.loads(data)

def serialize_simple(object):
    data = json.dumps(object, default=lambda o: o.__dict__, sort_keys=True)

    return json.loads(data)
