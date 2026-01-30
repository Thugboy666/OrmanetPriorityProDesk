from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class DataStore:
    clienti: Optional[pd.DataFrame] = None
    minord: Optional[pd.DataFrame] = None
    ordini: Optional[pd.DataFrame] = None


store = DataStore()
