from conversor_pdf_to_png import converte_pdf_to_png
from pathlib import Path
import logging
import sys

BASE_DIR = Path(__file__).parents[1]
sys.path.append(str(BASE_DIR))

from Tools.utils import set_logger
from Tools.utils import log_timer

PDFS_INPUT_DIR = BASE_DIR / "pdfs_para_conversao"
IMGS_OUTPUT_DIR = BASE_DIR / "imgs_convertidas"
LOG_PATH = BASE_DIR / "LOG/conversao_pdf_img.log"

logger_pronto = set_logger(LOG_PATH)

def main(logger: logging.Logger) -> None:
    with log_timer(logger_pronto, "Conversão de PDF para PNG"):
        converte_pdf_to_png(logger_pronto, PDFS_INPUT_DIR, IMGS_OUTPUT_DIR, "PNG", 300)


if __name__ == "__main__":
    main(logger_pronto)