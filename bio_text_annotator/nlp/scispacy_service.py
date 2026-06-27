import spacy


class SciSpaCyService:
    def __init__(self):
        self.nlp = spacy.load(
            "en_core_sci_lg"
        )


    def extract_entities(self, text: str) -> list[dict]:
        doc = self.nlp(text)
        entities = []

        for ent in doc.ents:
            entities.append(
                {
                    "text": ent.text,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "label": ent.label_,
                }
            )
        return entities