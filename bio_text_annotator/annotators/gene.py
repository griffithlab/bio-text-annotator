from bio_text_annotator.annotators.base import BaseAnnotator
from bio_text_annotator.nlp.scispacy_service import SciSpaCyService


class GeneAnnotator(BaseAnnotator):

    entity_type = "gene"

    def __init__(self):
        self.nlp = SciSpaCyService()


    def extract(self, text: str):
        entities = self.nlp.extract_entities(text)
        results = []

        for entity in entities:
            if entity["label"] not in [
                "GENE_OR_PROTEIN"
            ]:
                continue

            results.append(
                {
                    "type": self.entity_type,
                    "text": entity["text"],
                    "start": entity["start"],
                    "end": entity["end"],
                    "metadata": {
                        "source": "scispacy",
                        "label": entity["label"],
                    },
                }
            )
        return results