class Singleton:
    def __new__(cls,*a, **b):
        if hasattr(cls,'_inst'):
            return cls._inst
        else:
            cls._inst=super().__new__(cls,*a,**b)
            return cls._inst