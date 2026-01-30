# Ormanet Priority Pro Desk

Console MVP per importare e consultare clienti/ordini senza database.

## Avvio rapido (Windows)

> Nota: la cartella `runtime/` non è inclusa nel repo e va creata manualmente.

1. Creare l'ambiente runtime tramite lo script:
   ```powershell
   .\runtime\start.ps1
   ```
2. Avviare il backend:
   ```powershell
   uvicorn app.backend.main:app --reload
   ```
3. Aprire il browser su `http://localhost:8000`.

## Struttura

- `app/backend`: API FastAPI + template statici.
- `app/data/samples`: placeholder per dati di esempio.
- `scripts/codex_prompts`: note di bootstrap.

## Import richiesti

- Clienti (xlsx)
- Minimi ordine (xlsx)
- Ordini (xlsx)

I dati vengono caricati in memoria; la persistenza verrà aggiunta in futuro.
