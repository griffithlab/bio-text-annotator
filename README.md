# bio-text-annotator
A lightweight, local pipeline for extracting biomedical entities from scientific documents and generating structured reports.

This project is designed to run on user-provided documents (e.g. PDFs for a single publication) and produce a per-source summary of entities such as genes, variants, diseases, and drugs/chemicals. It is inspired by tools like PubTator, but intended to run fully locally and be modular/extensible.

## Overview
The goal of this project is to:
- Process a directory of documents associated with a single publication
- Extract text from PDFs and other supported formats
- Run biomedical named entity recognition (NER)
- Aggregate results into a simple, structured report
- Enable downstream tools to consume these reports (e.g. for UI display or further analysis)