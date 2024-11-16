from abc import ABC, abstractmethod

class Component(ABC):
    _registered_components = {}

    @abstractmethod
    def desc(self) -> str:
        pass

    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def attrs(self) -> dict:
        pass

    def __getattr__(self, attr):
        if attr in self.attrs():
            return self.__dict__.get(attr)
        raise AttributeError(f"{self.__class__.__name__} has no attribute {attr}")

    def __setattr__(self, attr, value):
        if attr in self.attrs():
            self.__dict__[attr] = value
        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {attr}")

    @abstractmethod
    def draw(self) -> str:
        pass
    
    @staticmethod
    def list():
        return [(name, comp().desc()) for name, comp in Component._registered_components.items()]

    @staticmethod
    def create(component_type: str):
        if component_type in Component._registered_components:
            return Component._registered_components[component_type]()
        print(f"Component type '{component_type}' is not registered.")
        return None

    @staticmethod
    def register(component_type: str, component_class: type):
        Component._registered_components[component_type] = component_class

    @staticmethod
    def unregister(component_type: str):
        if component_type in Component._registered_components:
            del Component._registered_components[component_type]
        else:
            print(f"Component type '{component_type}' is not registered.")