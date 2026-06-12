from bio_text_annotator.annotators.base import BaseAnnotator


class DiseaseAnnotator(BaseAnnotator):
    entity_type = "disease"

    def __init__(self):
        pass

    def extract(self, text: str):
        results = []

        return results
