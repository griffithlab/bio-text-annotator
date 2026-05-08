import re

from bio_text_annotator.annotators.base import BaseAnnotator


class VariantAnnotator(BaseAnnotator):
    entity_type = "variant"

    def __init__(self):
        # Common variant patterns
        self.patterns = [
            # Protein changes
            # Examples: p.V600E, p.R175H
            re.compile(r"\bp\.[A-Z][a-zA-Z]{0,2}\d+[A-Z][a-zA-Z]{0,2}\b"),

            # Coding DNA changes
            # Examples: c.1799T>A, c.35delG
            re.compile(r"\bc\.\d+[ACGT]>[ACGT]\b"),
            re.compile(r"\bc\.\d+del[ACGT]*\b"),
            re.compile(r"\bc\.\d+ins[ACGT]+\b"),

            # rsIDs
            # Examples: rs12345
            re.compile(r"\brs\d+\b", re.IGNORECASE),

            # Genomic notation
            # Examples: g.123456A>T
            re.compile(r"\bg\.\d+[ACGT]>[ACGT]\b")
        ]

    def extract(self, text: str):
        results = []

        for pattern in self.patterns:
            for match in pattern.finditer(text):
                results.append({
                    "type": self.entity_type,
                    "text": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "source": "regex"
                })

        return results