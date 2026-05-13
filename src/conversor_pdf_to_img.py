import fitz
from pathlib import Path
from PIL import Image
import io

BASE_DIR = Path(__file__).parents[1]

PDFS_INPUT_DIR = BASE_DIR / "pdfs_para_conversao"
IMGS_OUTPUT_DIR = BASE_DIR / "imgs_convertidas"

def converte_pdf_to_img(
    pdfs_path: str | Path,
    imgs_path: str | Path,
    img_format: str = "PNG",
    dpi: int = 300) -> None:
    
    for pdf_file in pdfs_path.glob("*.pdf"):
        doc = fitz.open(pdf_file)
        page = doc[0]

        matrix = fitz.Matrix(dpi / 72, dpi / 72) #72 é o dpi base do pdf
        pixmap = page.get_pixmap(matrix=matrix)

        image = Image.open(io.BytesIO(pixmap.tobytes()))
        output_file = imgs_path / f"{pdf_file.stem}.{img_format.lower()}"
        image.save(output_file, format=img_format)
        doc.close()


def main() -> None:
    converte_pdf_to_img(PDFS_INPUT_DIR, IMGS_OUTPUT_DIR, "PNG", 300)


if __name__ == "__main__":
    main()