class MetaConst(type):
    # def __getattr__(cls, key):
    #     return cls[key]

    def __setattr__(cls, key, value):
        raise TypeError
