from bio_text_annotator.ingestion.loader import load_documents
from bio_text_annotator.ingestion.pdf import extract_text
from bio_text_annotator.preprocessing.chunking import chunk_text
from bio_text_annotator.annotators.gene import GeneAnnotator
from bio_text_annotator.annotators.disease import DiseaseAnnotator
from bio_text_annotator.annotators.chemical import ChemicalAnnotator
from bio_text_annotator.annotators.variant import VariantAnnotator
from bio_text_annotator.reporting.aggregator import aggregate_entities
from bio_text_annotator.reporting.writer import write_report


def run_pipeline(
    input_dir: str,
    output_path: str,
    source_id: str,
    recursive: bool = False,
    formats: list[str] = None,
    verbose: bool = False,
    keep_temp: bool = False
):
    if formats is None:
        formats = ["pdf"]

    # 1. Load documents
    docs = load_documents(
        input_dir=input_dir,
        recursive=recursive,
        formats=formats
    )

    if verbose:
        print(f"[INFO] Found {len(docs)} documents")

    # 2. Initialize annotators
    annotators = [
        #GeneAnnotator(),
        #DiseaseAnnotator(),
        #ChemicalAnnotator(),
        VariantAnnotator(keep_temp=keep_temp)
    ]

    all_entities = []

    # 3. Process each document
    for doc_path in docs:
        if verbose:
            print(f"[INFO] Processing {doc_path}")

        text = extract_text(doc_path)
        chunks = chunk_text(text)
        
        for annotator in annotators:
            if annotator.requires_full_document:
                entities = annotator.extract(text)
                all_entities.extend(entities)
            else:
                for chunk in chunks:
                    entities = annotator.extract(chunk)
                    all_entities.extend(entities)

    # 4. Aggregate results
    report = aggregate_entities(
        entities=all_entities,
        source_id=source_id
    )

    # 5. Write output
    write_report(report, output_path)

    if verbose:
        print(f"[INFO] Report written to {output_path}")