import argparse
from bio_text_annotator import run_pipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract biomedical entities from a directory of documents"
    )

    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing documents for a single source"
    )

    parser.add_argument(
        "--source-id",
        required=True,
        help="Identifier for the publication/source being processed"
    )

    parser.add_argument(
        "--output",
        default="./outputs/report.json",
        help="Path to output report (default: ./outputs/report.json)"
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively search for documents"
    )

    parser.add_argument(
        "--formats",
        nargs="+",
        default=["pdf"],
        help="File formats to include (default: pdf)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep temporary files generated during processing (for debugging)"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    run_pipeline(
        input_dir=args.input_dir,
        output_path=args.output,
        source_id=args.source_id,
        recursive=args.recursive,
        formats=args.formats,
        verbose=args.verbose,
        keep_temp=args.keep_temp
    )


if __name__ == "__main__":
    main()