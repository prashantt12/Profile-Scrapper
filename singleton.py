class Singleton(type):
    _Instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._Instances:
            cls._Instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._Instances[cls]