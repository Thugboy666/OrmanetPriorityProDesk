from io import BytesIO

import pandas as pd


def parse_xlsx(data: bytes) -> pd.DataFrame:
    return pd.read_excel(BytesIO(data), engine="openpyxl")
