from python_models.base import MyMetaclass
from .const import EventType
from python_models.base import factory_function





if __name__ == '__main__':
    t = EventType.T1
    print(factory_function(t))