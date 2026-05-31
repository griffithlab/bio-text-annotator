from bio_text_annotator.annotators.base import BaseAnnotator
from bio_text_annotator.external.tmvar.service import TMVarService


class VariantAnnotator(BaseAnnotator):

    entity_type = "variant"
    requires_full_document = True

    def __init__(self):
        self.tmvar = TMVarService()

    def extract(self, text: str):
        return self.tmvar.annotate(text)