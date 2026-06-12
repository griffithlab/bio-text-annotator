from bio_text_annotator.ingestion.loader import load_documents
from bio_text_annotator.ingestion.pdf import extract_text
from bio_text_annotator.preprocessing.chunking import chunk_text
from bio_text_annotator.annotators.gene import GeneAnnotator
from bio_text_annotator.annotators.disease import DiseaseAnnotator
from bio_text_annotator.annotators.chemical import ChemicalAnnotator
from bio_text_annotator.annotators.variant import VariantAnnotator
from bio_text_annotator.reporting.aggregator import aggregate_entities
from bio_text_annotator.reporting.writer import write_report

import re

_HEAP_RE = re.compile(r"^\d+[MG]$", re.IGNORECASE)


def validate_heap_size(heap_size: str):
    if not _HEAP_RE.match(heap_size):
        raise ValueError(
            f"Invalid heap_size '{heap_size}'. Expected format like '2G' or '512M'."
        )

    value = int(heap_size[:-1])
    unit = heap_size[-1].upper()

    if unit == "G" and value < 1:
        raise ValueError("heap_size must be at least 1G")

    if unit == "M" and value < 512:
        raise ValueError("heap_size too small (minimum ~512M recommended)")


def run_pipeline(
    input_dir: str,
    output_path: str,
    source_id: str,
    recursive: bool = False,
    formats: list[str] = None,
    verbose: bool = False,
    keep_temp: bool = False,
    output_mode: str = "document",
    heap_size: str = "5G",
):
    validate_heap_size(heap_size)

    if formats is None:
        formats = ["pdf"]

    # 1. Load documents
    docs = load_documents(input_dir=input_dir, recursive=recursive, formats=formats)

    if verbose:
        print(f"[INFO] Found {len(docs)} documents")

    # 2. Initialize annotators
    annotators = [
        # GeneAnnotator(),
        # DiseaseAnnotator(),
        # ChemicalAnnotator(),
        VariantAnnotator(keep_temp=keep_temp, heap_size=heap_size)
    ]

    documents = []

    # 3. Process each document
    for doc_path in docs:
        if verbose:
            print(f"[INFO] Processing {doc_path}")

        text = extract_text(doc_path)
        chunks = chunk_text(text)

        doc_entities = []

        for annotator in annotators:
            if annotator.requires_full_document:
                entities = annotator.extract(text)
            else:
                entities = []
                for chunk in chunks:
                    entities.extend(annotator.extract(chunk))

            doc_entities.extend(entities)

        documents.append({"doc_id": str(doc_path), "entities": doc_entities})

    # 4. Aggregate results
    report = aggregate_entities(
        documents=documents, source_id=source_id, output_mode=output_mode
    )

    # 5. Write output
    write_report(report, output_path)

    if verbose:
        print(f"[INFO] Report written to {output_path}")
