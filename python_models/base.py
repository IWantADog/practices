from .const import EventType

_class_map = {}


class MyMetaclass(type):
    def __new__(cls, name, base, attrs):
        new_class = super().__new__(cls, name, base, attrs)
        if "c_type" in attrs:
            _class_map[attrs["c_type"]] = new_class
        return new_class


def factory_function(event_type):
    if event_type in _class_map:
        return _class_map[event_type]
    print(_class_map)
    raise ValueError(f"undefined event type: {event_type}")

class T1(metaclass=MyMetaclass):
    c_type = EventType.T1

class T2(metaclass=MyMetaclass):
    c_type = EventType.T2
