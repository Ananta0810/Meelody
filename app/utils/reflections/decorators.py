def memoize(f):
    def wrapped(*args, **kwargs):
        if hasattr(wrapped, '_cachedValue'):
            return wrapped._cachedValue
        result = f(*args, **kwargs)
        wrapped._cachedValue = result
        return result

    return wrapped


class staticproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class memoizeStaticProperty(property):
    def __get__(self, cls, owner):
        methodId = classmethod(self.fget).__str__()
        if hasattr(self, methodId):
            return getattr(self, methodId)
        value = classmethod(self.fget).__get__(None, owner)()
        setattr(self, methodId, value)
        return value


def memoizeResult(f):
    def wrapped(*args, **kwargs):
        if not hasattr(wrapped, '_cachedValue'):
            wrapped._cachedValue = {}

        key = f"{args} - {kwargs}"
        if key in wrapped._cachedValue:
            return wrapped._cachedValue[key]

        result = f(*args, **kwargs)
        wrapped._cachedValue[key] = result
        return result

    return wrapped


def returnOnFailed(value: any):
    def decorate(f):
        def applicator(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                return value

        return applicator

    return decorate


def suppressException(f):
    def applicator(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            from app.utils.others import Logger
            Logger.error(e)
            pass

    return applicator
