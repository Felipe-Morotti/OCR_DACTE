import pandas as pd
import logging
from pathlib import Path


def salvarCSV(parsed: dict[str, dict], output_path: Path, logger: logging.Logger) -> None:
    df = pd.DataFrame(parsed.values())
    df.to_csv(output_path, index=False, encoding="utf-8")

