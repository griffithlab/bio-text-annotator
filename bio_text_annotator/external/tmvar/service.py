from pathlib import Path
import subprocess
import tempfile

from bio_text_annotator.preprocessing.bioc import text_to_bioc


class TMVarService:

    def __init__(self):
        self.tmvar_root = (
            Path(__file__).resolve().parent
        )

        self.jar_path = (
            self.tmvar_root / "tmVar.jar"
        )

    def annotate(self, text: str):
        with tempfile.TemporaryDirectory() as tmpdir:

            tmpdir = Path(tmpdir)

            input_dir = tmpdir / "input"
            output_dir = tmpdir / "output"

            input_dir.mkdir()
            output_dir.mkdir()

            bioc_path = input_dir / "document.xml"

            bioc_path.write_text(
                text_to_bioc(text),
                encoding="utf-8"
            )

            subprocess.run(
                [
                    "java",
                    "-Xmx5G",
                    "-Xms5G",
                    "-jar",
                    str(self.jar_path),
                    str(input_dir),
                    str(output_dir),
                ],
                cwd=self.tmvar_root,
                check=True,
            )

            return self._parse_output(output_dir)

    def _parse_output(self, output_dir):
        raise NotImplementedError