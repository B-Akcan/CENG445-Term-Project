class Component():
    _registered_components = {}

    def desc(self) -> str:
        pass

    def type(self) -> str:
        pass

    def attrs(self) -> dict:
        pass

    def __getattr__(self, attr):
        if attr not in self.attrs():
            raise AttributeError(f"Class '{self.__class__.__name__}' has no attribute '{attr}'")
        super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        if attr not in self.attrs():
            raise AttributeError(f"Class '{self.__class__.__name__}' has no attribute '{attr}'")
        super().__setattr__(attr, value)

    def draw(self) -> str:
        pass
    
    @classmethod
    def list(cls):
        print( [(name, comp.desc()) for name, comp in cls._registered_components.items()] )

    @classmethod
    def create(cls, component_type: str, *p, **kw):
        if component_type in cls._registered_components:
            return cls._registered_components[component_type](*p, **kw)
        raise ValueError(f"Component type '{component_type}' is not registered.")

    @classmethod
    def register(cls, component_type: str, component_class: type):
        cls._registered_components[component_type] = component_class

    @classmethod
    def unregister(cls, component_type: str):
        if component_type in cls._registered_components:
            del cls._registered_components[component_type]
        else:
            raise ValueError(f"Component type '{component_type}' is already unregistered.")