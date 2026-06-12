# bio-text-annotator

A lightweight, local pipeline for extracting biomedical entities from scientific documents and generating structured reports.

This project processes user-provided documents (e.g., PDFs for a single publication) and extracts biomedical entities such as genetic variants. It is inspired by PubTator-style pipelines but designed to run fully locally and remain modular and extensible.

---

## Current Capabilities

At present, the pipeline supports:

- Variant extraction only
- Powered by TMVar3 (Java CRF-based model)
- Detection of:
  - DNA mutations (e.g., `c.233A>G`)
  - Protein mutations (e.g., `p.Asn78Ser`)
  - Deletions, substitutions, frameshifts, nonsense variants
- Extraction from full-text biomedical PDFs via text parsing + BioC conversion

Additional entity types (genes, diseases, chemicals) are planned but not yet enabled.

---

## Pipeline Overview

The system performs the following steps:

1. Load documents from an input directory  
2. Extract text from PDFs using PyMuPDF  
3. Normalize and clean text for biomedical NLP  
4. Convert text to BioC format (TMVar-compatible)  
5. Run TMVar3 (Java CRF pipeline)  
6. Parse PubTator output into structured entities  
7. Aggregate results into a JSON report  

---

## Installation

### Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Java Requirement

TMVar3 requires:

- Java 8+ (recommended Java 11 or 17)
- Sufficient heap memory (default uses `-Xmx5G`)

---

## Usage

### CLI

Run the pipeline using:

```bash
python3 -m bio_text_annotator.cli \
    --input-dir tests/test_data/ \
    --source-id nihms-1892649 \
    --verbose
```

### CLI Arguments
- ```--input-dir```
    
    Directory containing documents for a single source (PDFs only currently)
- ```--source-id```

    Identifier for the dataset/publication being processed
- ```--output```

    Output path for JSON report
    Default: ```./outputs/report.json```
- ```--recursive```
    
    Recursively search input directory for documents
- ```--formats```
    
    File types to include (PDFs only currently)
- ```--verbose```
    
    Enable debug logging
- ```--keep-temp```
    
    Preserve intermediate TMVar files for debugging
- ```--output-mode```

    Output structure format:
  - ```document``` (default): grouped per document
  - ```flat```: fully aggregated entity list

- ```--heap-size```

    Java heap size for TMVar3 execution (e.g., `2G`, `5G`, `8G`).
    Default: `5G` (recommended).
    
    Adjust based on available system memory and document size.

### Output Format
The pipeline produces a structured JSON report:
```bash
{
  "source_id": "nihms-1892649",
  "documents": [
    {
      "doc_id": "...",
      "entities": [
        {
          "type": "variant",
          "text": "c.233A>G",
          "start": 19563,
          "end": 19571,
          "subtype": "SUB",
          "normalized_id": "c|SUB|A|233|G"
        }
      ]
    }
  ]
}
```