from bio_text_annotator.annotators.base import BaseAnnotator
from bio_text_annotator.external.tmvar.service import TMVarService


class VariantAnnotator(BaseAnnotator):

    entity_type = "variant"
    requires_full_document = True

    def __init__(self, keep_temp: bool = False, heap_size: str = "5G"):
        self.tmvar = TMVarService(keep_temp=keep_temp, heap_size=heap_size)

    def extract(self, text: str):
        results = self.tmvar.annotate(text)
        entities = []

        for item in results:
            metadata = {}

            if "subtype" in item:
                metadata["subtype"] = item["subtype"]

            if "normalized_id" in item:
                metadata["normalized_id"] = item["normalized_id"]

            entities.append(
                {
                    "type": self.entity_type,
                    "text": item["text"],
                    "start": item.get("start"),
                    "end": item.get("end"),
                    "metadata": metadata,
                }
            )

        return entities
