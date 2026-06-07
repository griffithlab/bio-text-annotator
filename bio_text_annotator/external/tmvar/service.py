from pathlib import Path
import subprocess
import shutil

from bio_text_annotator.external.tmvar.model_manager import ensure_models
from bio_text_annotator.preprocessing.bioc import text_to_bioc


class TMVarService:
    def __init__(self, keep_temp: bool = False):
        ensure_models()

        self.tmvar_root = Path(__file__).resolve().parent

        self.jar_path = self.tmvar_root / "tmVar.jar"

        self.keep_temp = keep_temp

        if not self.jar_path.exists():
            raise FileNotFoundError(
                f"Missing TMVar jar: {self.jar_path}"
            )

        self.work_dir = self.tmvar_root / "tmp"

    def annotate(self, text: str):
        # TMVar expects its temporary files relative to its root directory.
        # Clean previous run artifacts.
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir)

        input_dir = self.work_dir / "input"
        output_dir = self.work_dir / "output"

        input_dir.mkdir(parents=True)
        output_dir.mkdir()

        try:
            bioc_path = input_dir / "document.xml"

            bioc_path.write_text(
                text_to_bioc(text),
                encoding="utf-8"
            )

            result = subprocess.run(
                [
                    "java",
                    "-Xmx5G",
                    "-Xms5G",
                    "-cp",
                    "tmVar.jar:lib/*:CRF:.",
                    "tmVarlib.tmVar",
                    str(input_dir),
                    str(output_dir),
                ],
                cwd=self.tmvar_root,
                text=True,
                capture_output=True,
            )

            if result.returncode != 0:
                print("TMVar STDOUT:")
                print(result.stdout)

                print("TMVar STDERR:")
                print(result.stderr)

                raise RuntimeError(
                    f"TMVar failed with exit code {result.returncode}"
                )

            return self._parse_output(output_dir)
        finally:
            if not self.keep_temp and self.work_dir.exists():
                shutil.rmtree(self.work_dir)

    def _parse_output(self, output_dir):
        output_file = output_dir / "document.xml.PubTator"

        if not output_file.exists():
            raise FileNotFoundError(
                f"TMVar output not found: {output_file}"
            )

        entities = []

        with open(output_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                parts = line.split("\t")

                # Header lines:
                # document|abstract|text
                if len(parts) < 6:
                    continue

                document_id, start, end, text, entity_type, identifier = parts[:6]

                if entity_type not in {
                    "DNAMutation",
                    "ProteinMutation",
                    "SNP",
                    "DNAAllele",
                }:
                    continue

                entities.append(
                    {
                        "type": "variant",
                        "text": text,
                        "start": int(start),
                        "end": int(end),
                        "subtype": entity_type,
                        "normalized_id": identifier,
                    }
                )

        return entities