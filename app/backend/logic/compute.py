from __future__ import annotations

from typing import Any, Iterable, Optional

import pandas as pd

from app.backend.logic import rules


def _normalize(text: Any) -> str:
    if text is None:
        return ""
    return str(text).strip().lower()


def find_column(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[str]:
    normalized_candidates = {c.strip().lower() for c in candidates}
    for column in df.columns:
        normalized_column = str(column).strip().lower()
        if normalized_column in normalized_candidates:
            return column
        if any(candidate in normalized_column for candidate in normalized_candidates):
            return column
    return None


def search_clienti(clienti_df: pd.DataFrame, query: str) -> list[dict]:
    ragione_column = find_column(clienti_df, [
        "ragione sociale",
        "ragionesociale",
        "cliente",
        "denominazione",
    ])
    if ragione_column is None:
        return []

    normalized_query = _normalize(query)
    results = []
    for value in clienti_df[ragione_column].dropna().unique():
        if normalized_query in _normalize(value):
            results.append({"ragione_sociale": str(value)})
    return results[:20]


def _lookup_row(df: pd.DataFrame, ragione_sociale: str) -> Optional[pd.Series]:
    ragione_column = find_column(df, [
        "ragione sociale",
        "ragionesociale",
        "cliente",
        "denominazione",
    ])
    if ragione_column is None:
        return None

    normalized_target = _normalize(ragione_sociale)
    matches = df[df[ragione_column].apply(_normalize) == normalized_target]
    if matches.empty:
        return None
    return matches.iloc[0]


def _extract_value(row: Optional[pd.Series], df: Optional[pd.DataFrame], candidates: list[str]) -> Any:
    if row is None or df is None:
        return None
    column = find_column(df, candidates)
    if column is None:
        return None
    return row.get(column)


def build_cliente_scheda(
    clienti_df: pd.DataFrame,
    minord_df: Optional[pd.DataFrame],
    ordini_df: Optional[pd.DataFrame],
    ragione_sociale: str,
) -> Optional[dict]:
    cliente_row = _lookup_row(clienti_df, ragione_sociale)
    if cliente_row is None:
        return None

    listino = _extract_value(
        cliente_row,
        clienti_df,
        ["listino", "listino prezzo", "listino prezzi"],
    )

    porto_raw = _extract_value(
        cliente_row,
        clienti_df,
        ["porto franco", "porto_franco", "portofranco"],
    )
    porto_franco = rules.normalize_porto_franco(porto_raw)

    minord_value = None
    if minord_df is not None:
        minord_row = _lookup_row(minord_df, ragione_sociale)
        minord_value = _extract_value(
            minord_row,
            minord_df,
            ["min ord", "minordine", "minimo ordine"],
        )

    drop_flag = False
    if ordini_df is not None:
        ragione_column = find_column(ordini_df, [
            "ragione sociale",
            "ragionesociale",
            "cliente",
            "denominazione",
        ])
        drop_column = find_column(ordini_df, ["drop", "drop shipment", "spedizione drop"])
        if ragione_column is not None:
            matches = ordini_df[ordini_df[ragione_column].apply(_normalize) == _normalize(ragione_sociale)]
            if drop_column is not None and not matches.empty:
                drop_flag = matches[drop_column].apply(lambda value: _normalize(value) in {"si", "s", "1", "true"}).any()

    return {
        "ragione_sociale": str(ragione_sociale),
        "listino": listino,
        "porto_franco": porto_franco,
        "porto_assegnato": porto_franco != "none",
        "min_ord": minord_value,
        "drop": drop_flag,
    }
