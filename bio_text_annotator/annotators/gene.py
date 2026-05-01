from bio_text_annotator.annotators.base import BaseAnnotator


class GeneAnnotator(BaseAnnotator):
    entity_type = "gene"

    def __init__(self):
        pass

    def extract(self, text: str):
        results = []

        return results