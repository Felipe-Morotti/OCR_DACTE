#LightOnOCR-2

import torch
from transformers import LightOnOcrForConditionalGeneration, LightOnOcrProcessor
from PIL import Image
from pathlib import Path
import pandas as pd
import re
from bs4 import BeautifulSoup
import logging
from logger_config import set_logger
from logger_config import log_timer


BASE_DIR = Path(__file__).parents[1]
IMGS_PATH = BASE_DIR / "imgs_convertidas"
CSV_OUTPUT_PATH = BASE_DIR / "DACTEsCSV/DACTEs.csv"
LOG_PATH = BASE_DIR / "LOG/dacte_ocr.log"

logger_pronto = set_logger(LOG_PATH)

def performOCR(imgs_path: str | Path, logger: logging.Logger) -> dict[str, str]:

    #configuração do hardware e precisão
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16

    #carregamento do modelo e processador
    #model = carrega os pesos do LightOnOCR-2-1B
    #processor = tradutor que prepara a imagem e o texto
    model = LightOnOcrForConditionalGeneration.from_pretrained("lightonai/LightOnOCR-2-1B", torch_dtype=dtype).to(device)
    processor = LightOnOcrProcessor.from_pretrained("lightonai/LIghtOnOCR-2-1B")

    results = {}

    for i, img in enumerate(imgs_path.glob("*.png"), 1):
        image = Image.open(img)
        logger.info(f"Imagem {i} carregada. \u2705")

        conversation = [{"role": "user", "content": [
        {"type": "image", "image": image},
        {"type": "text", "text": "Extract all text from this image."}]}]

        prompt = processor.apply_chat_template(
            conversation,
            add_generation_prompt=True,
            tokenize=False,
        )

        inputs = processor(text=prompt, images=image, return_tensors="pt")

        inputs = {k: v.to(device=device, dtype=dtype) if v.is_floating_point() else v.to(device) for k, v in inputs.items()}

        output_ids = model.generate(**inputs, max_new_tokens=2048)
        generated_ids = output_ids[0, inputs["input_ids"].shape[1]:]

        output_text = processor.decode(generated_ids, skip_special_tokens=True)

        
        logger.info(f"OCR da imagem {i} concluída. \u2705")

        results[img.name] = output_text
    
    logger.info(f"OCR concluído com sucesso. \u2705")
    return results


def parse_results(results: dict[str, str], logger: logging.Logger) -> dict[str, dict]:
    logger.info(f"Iniciando o parsing de {len(results)} arquivos. \u26A0")

    parsed = {}

    modal_map = {"RODOVIÁRIO": 1, "AÉREO": 2, "AQUAVIÁRIO": 3, "FERROVIÁRIO": 4, "DUTOVIÁRIO": 5}

    for filename, html in results.items():
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        def find(pattern, default=None):
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            return match.group(1).strip() if match else default

        def cnpj_or_cpf(value):
            if value and "/" in value:
                return value, None   # é CNPJ
            return None, value       # é CPF

        # emitente: aparece no cabeçalho antes de "DACTE"
        header = text.split("DACTE")[0] if "DACTE" in text else ""
        emit_nome  = re.search(r"^(.+?)\s+CNPJ:", header, re.IGNORECASE)
        emit_cnpj  = re.search(r"CNPJ:\s*([\d\.\/\-]+)", header, re.IGNORECASE)

        # remetente
        rem_nome   = find(r"REMETENTE\s+(.+?)\s+ENDERECO")
        rem_doc    = find(r"REMETENTE.+?CNPJ/CPF\s+([\d\.\/\-]+)")
        rem_cnpj, rem_cpf = cnpj_or_cpf(rem_doc)

        # destinatário
        dest_nome  = find(r"DESTINATÁRIO\s+(.+?)\s+ENDERECO")
        dest_doc   = find(r"DESTINATÁRIO.+?CNPJ/CPF\s+([\d\.\/\-]+)")
        dest_cnpj, dest_cpf = cnpj_or_cpf(dest_doc)

        # modal
        modal_str  = find(r"MODAL\s+(\w+)")
        modal_num  = modal_map.get(modal_str.upper(), None) if modal_str else None

        parsed[filename] = {
            "arquivo":    filename,
            "nCT":        find(r"NÚMERO\s+(\d+)"),
            "cCT":        None,  # não consta no DACTE impresso
            "CFOP":       find(r"CFOP\s*-[^0-9]*(\d{4})"),
            "dhEmi":      find(r"EMISSÃO\s+([\d\/]+\s[\d\:]+)"),
            "tpAmb":      None,  # não consta no DACTE impresso
            "modal":      modal_num,
            "xMunIni":    find(r"INÍCIO DA PRESTAÇÃO\s+([^-]+?)\s*-\s*[A-Z]{2}"),
            "UFIni":      find(r"INÍCIO DA PRESTAÇÃO\s+[^-]+-\s*([A-Z]{2})"),
            "xMunFim":    find(r"TÉRMINO DA PRESTAÇÃO\s+([^-]+?)\s*-\s*[A-Z]{2}"),
            "UFFim":      find(r"TÉRMINO DA PRESTAÇÃO\s+[^-]+-\s*([A-Z]{2})"),
            "emit_CNPJ":  emit_cnpj.group(1).strip() if emit_cnpj else None,
            "emit_xNome": emit_nome.group(1).strip() if emit_nome else None,
            "rem_CNPJ":   rem_cnpj,
            "rem_CPF":    rem_cpf,
            "rem_xNome":  rem_nome,
            "dest_CNPJ":  dest_cnpj,
            "dest_CPF":   dest_cpf,
            "dest_xNome": dest_nome,
            "vTPrest":    find(r"VALOR TOTAL DA PRESTAÇÃO\s*([\d\.,]+)"),
            "vRec":       find(r"VALOR A RECEBER\s*([\d\.,]+)"),
            "vCarga":     find(r"VALOR TOTAL DA CARGA\s*([\d\.,]+)"),
            "proPred":    find(r"PRODUTO PREDOMINANTE\s+(.+?)\s{2}"),
            "CST":        find(r"CST\s*[\|:]?\s*(\d+)"),
            "vBC":        find(r"BASE DE CÁLCULO\s*([\d\.,]+)"),
            "pICMS":      find(r"ALÍQUOTA\s*([\d\.,]+)"),
            "vICMS":      find(r"VALOR DO ICMS\s*([\d\.,]+)"),
            "placa":      find(r"PLACA\s*([A-Z]{3}[\-]?\d[\w]\d{2})"),
            "UF_veiculo": find(r"PLACA\s+[A-Z0-9\-]+\s+([A-Z]{2})"),
        }

    logger.info(f"Parsing concluído com sucesso. \u2705")
    return parsed

def salvarCSV(parsed: dict[str, dict], output_path: Path, logger: logging.Logger) -> None:
    df = pd.DataFrame(parsed.values())
    df.to_csv(output_path, index=False, encoding="utf-8")

    logger.info(f"Salvo em CSV. \u2705")

def main() -> None:
    with log_timer(logger_pronto, "OCR dos DACTEs."):
        dados_raw = performOCR(IMGS_PATH, logger_pronto)

    with log_timer(logger_pronto, "Parseamento dos dados."):
        parseado = parse_results(dados_raw, logger_pronto)

    with log_timer(logger_pronto, "Salvamento dos dados em formato CSV."):
        salvarCSV(parseado, CSV_OUTPUT_PATH, logger_pronto)

    logger_pronto.info("Processo concluído com sucesso. \u2705")

if __name__ == "__main__":
    main()