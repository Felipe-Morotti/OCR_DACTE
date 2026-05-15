import logging
from bs4 import BeautifulSoup
import re

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

    return parsed
