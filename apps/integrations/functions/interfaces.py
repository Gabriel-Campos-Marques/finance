from abc import ABC, abstractmethod

class FileImporterInterface(ABC):
    @abstractmethod
    def process(self, *args, **kwargs):
        """Process the file and import its contents."""
        pass
