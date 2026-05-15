from ocr_dacte import performOCR
from parser_output_do_ocr import parse_results
from salvar_csv import salvarCSV
from pathlib import Path
import logging
import sys

BASE_DIR = Path(__file__).parents[1]

sys.path.append(str(BASE_DIR))

from Tools.utils import set_logger
from Tools.utils import log_timer

IMGS_PATH = BASE_DIR / "imgs_convertidas"
CSV_OUTPUT_PATH = BASE_DIR / "DACTEsCSV/DACTEs.csv"
LOG_PATH = BASE_DIR / "LOG/dacte_ocr.log"

logger_pronto = set_logger(LOG_PATH)

def main(logger: logging.Logger) -> None:
    with log_timer(logger_pronto, "OCR dos DACTEs."):
        dados_raw = performOCR(IMGS_PATH, logger_pronto)

    with log_timer(logger_pronto, "Parseamento dos dados."):
        parseado = parse_results(dados_raw, logger_pronto)

    with log_timer(logger_pronto, "Salvamento dos dados em formato CSV."):
        salvarCSV(parseado, CSV_OUTPUT_PATH, logger_pronto)

    logger_pronto.info("Processo concluído com sucesso. \u2705")

if __name__ == "__main__":
    main(logger_pronto)