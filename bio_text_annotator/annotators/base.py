from abc import ABC, abstractmethod


class BaseAnnotator(ABC):
    entity_type: str

    requires_full_document = False

    @abstractmethod
    def extract(self, text: str) -> list[dict]:
        pass
