# app/ocr/base_ocr_engine.py

from abc import ABC, abstractmethod

class BaseOCREngine(ABC):
    @abstractmethod
    async def extract_text(self, file_path: str) -> str:
        """
        Extract raw OCR text from the file at the given path.
        """
        pass
