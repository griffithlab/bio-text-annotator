from abc import ABC, abstractmethod


class BaseAnnotator(ABC):
    entity_type: str

    @abstractmethod
    def extract(self, text: str) -> list[dict]:
        """
        Returns:
            List of entities in standard format:
            {
                "type": str,
                "text": str,
                "start": int (optional),
                "end": int (optional)
            }
        """
        pass