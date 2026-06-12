from pathlib import Path
import urllib.request


MODEL_DIR = Path(__file__).parent / "CRF"

MODELS = {
    "MentionExtractionUB.fulltext.Model": "https://github.com/griffithlab/bio-text-annotator/releases/download/v1.0.0/MentionExtractionUB.fulltext.Model",
    "MentionExtractionUB.Model": "https://github.com/griffithlab/bio-text-annotator/releases/download/v1.0.0/MentionExtractionUB.Model",
}


def ensure_models():
    MODEL_DIR.mkdir(exist_ok=True)

    missing = []

    for filename in MODELS:
        if not (MODEL_DIR / filename).exists():
            missing.append(filename)

    if not missing:
        return

    print("[INFO] TMVar models missing. Downloading...")

    for filename in missing:
        url = MODELS[filename]
        destination = MODEL_DIR / filename

        urllib.request.urlretrieve(url, destination)

    print("[INFO] TMVar models installed.")
