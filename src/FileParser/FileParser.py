from pdfminer.high_level import extract_text
from pathlib import Path

class FileParser:
    @staticmethod
    def GetRawText(file: Path) -> str:
        """
        Fastest way to extract raw text from a PDF using pdfminer.

        Args:
            file (Path): Path object of the pdf file.

        Returns:
            str: Extracted plain text from the PDF.
        """
        return extract_text(str(file))