from abc import abstractmethod, ABC


# base class inherited by all low level connection objects
class UOSInterface(metaclass=ABC):

    @abstractmethod
    def execute_instruction(self, address: int, payload: [int], lazy_loaded=True) -> (bool, {}):
        pass
