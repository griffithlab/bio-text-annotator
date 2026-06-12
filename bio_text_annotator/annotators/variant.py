from bio_text_annotator.annotators.base import BaseAnnotator
from bio_text_annotator.external.tmvar.service import TMVarService


class VariantAnnotator(BaseAnnotator):

    entity_type = "variant"
    requires_full_document = True

    def __init__(self, keep_temp: bool = False, heap_size: str = "5G"):
        self.tmvar = TMVarService(keep_temp=keep_temp, heap_size=heap_size)

    def extract(self, text: str):
        return self.tmvar.annotate(text)
