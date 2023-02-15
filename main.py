if __name__ == '__main__':
    from python_models.base import factory_function
    from python_models.const import EventType

    print(factory_function(EventType.T1))