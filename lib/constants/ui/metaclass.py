class SingletonConst(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonConst, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def __setattr__(cls, key, value):
        raise TypeError

    @property
    def my_data(cls):
        if getattr(cls, "_MY_DATA", None) is None:
            my_data = ...  # costly database call
            cls._MY_DATA = my_data
        return cls._MY_DATA
