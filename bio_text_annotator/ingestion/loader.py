from pathlib import Path


def load_documents(
    input_dir: str, recursive: bool = False, formats: list[str] | None = None
) -> list[Path]:
    """
    Load documents from a directory matching the specified formats.

    Args:
        input_dir: Directory containing source documents.
        recursive: Whether to search subdirectories recursively.
        formats: List of allowed file extensions (e.g. ["pdf", "txt"]).

    Returns:
        List of matching document paths.
    """

    if formats is None:
        formats = ["pdf"]

    input_path = Path(input_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    if not input_path.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_dir}")

    # Normalize extensions
    formats = {ext.lower().lstrip(".") for ext in formats}

    documents = []

    if recursive:
        iterator = input_path.rglob("*")
    else:
        iterator = input_path.glob("*")

    for path in iterator:
        if not path.is_file():
            continue

        extension = path.suffix.lower().lstrip(".")

        if extension in formats:
            documents.append(path)

    return sorted(documents)
