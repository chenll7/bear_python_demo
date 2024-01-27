from abc import ABC, abstractmethod

class MyControllerError(Exception): pass


class AbstractController(ABC):
    @abstractmethod
    def main(self):
        pass