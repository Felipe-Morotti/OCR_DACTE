import fitz
from pathlib import Path
from PIL import Image
import io
import logging

def converte_pdf_to_png(
    logger: logging.Logger,
    pdfs_path: str | Path,
    imgs_path: str | Path,
    img_format: str = "PNG",
    dpi: int = 300) -> None:
    
    for i, pdf_file in enumerate(pdfs_path.glob("*.pdf"), 1):
        doc = fitz.open(pdf_file)
        page = doc[0]
        logger.info(f"PDF {i} sendo convertido.")

        matrix = fitz.Matrix(dpi / 72, dpi / 72) #72 é o dpi base do pdf
        pixmap = page.get_pixmap(matrix=matrix)

        image = Image.open(io.BytesIO(pixmap.tobytes()))
        output_file = imgs_path / f"{pdf_file.stem}.{img_format.lower()}"
        image.save(output_file, format=img_format)
        doc.close()
        logger.info(f"Imagem {1} gerada. \u2705")


