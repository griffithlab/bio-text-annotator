from bio_text_annotator.annotators.base import BaseAnnotator


class VariantAnnotator(BaseAnnotator):
    entity_type = "variant"

    def __init__(self):
        pass

    def extract(self, text: str):
        results = []
        
        return results