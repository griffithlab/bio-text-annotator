from abc import ABC, abstractmethod


class BaseAnnotator(ABC):
    entity_type: str

    requires_full_document = False

    def extract(self, text: str):
        raise NotImplementedError
