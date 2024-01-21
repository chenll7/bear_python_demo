from abc import ABC, abstractmethod

class AbstractController(ABC):
    @abstractmethod
    def main(self):
        pass