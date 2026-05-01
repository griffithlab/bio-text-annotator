from bio_text_annotator.annotators.base import BaseAnnotator


class ChemicalAnnotator(BaseAnnotator):
    entity_type = "chemical"

    def __init__(self):
        pass

    def extract(self, text: str):
        results = []

        return results