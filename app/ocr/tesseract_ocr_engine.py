# app/ocr/tesseract_ocr_engine.py

import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from app.ocr.base_ocr_engine import BaseOCREngine
from app.utils.logger import get_logger

logger = get_logger("TesseractOCR")

class TesseractOCREngine(BaseOCREngine):
    async def extract_text(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        logger.info(f"Extracting text from file: {file_path} (ext: {ext})")

        try:
            if ext == ".pdf":
                images = convert_from_path(file_path)
                logger.info(f"PDF has {len(images)} pages")

                text = "\n".join(pytesseract.image_to_string(img) for img in images)

            else:
                image = Image.open(file_path)
                logger.info(f"Image format: {image.format}, size: {image.size}")

                text = pytesseract.image_to_string(image)

            logger.debug(f"OCR Text Extracted: {text[:300]}...")  # Show first 300 chars
            return text

        except Exception as e:
            logger.error(f"OCR extraction failed: {e}", exc_info=True)
            raise
