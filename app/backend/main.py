from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.backend.io import importers
from app.backend.logic import compute
from app.backend.logic.models import store

app = FastAPI(title="OrmanetPriorityProDesk")

app.mount("/static", StaticFiles(directory="app/backend/web/static"), name="static")

templates = Jinja2Templates(directory="app/backend/web/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/import/clienti")
async def import_clienti(file: UploadFile = File(...)) -> dict:
    data = await file.read()
    store.clienti = importers.parse_xlsx(data)
    return {"rows": int(store.clienti.shape[0])}


@app.post("/api/import/minord")
async def import_minord(file: UploadFile = File(...)) -> dict:
    data = await file.read()
    store.minord = importers.parse_xlsx(data)
    return {"rows": int(store.minord.shape[0])}


@app.post("/api/import/ordini")
async def import_ordini(file: UploadFile = File(...)) -> dict:
    data = await file.read()
    store.ordini = importers.parse_xlsx(data)
    return {"rows": int(store.ordini.shape[0])}


@app.get("/api/clienti")
def search_clienti(q: str = "") -> list[dict]:
    if store.clienti is None:
        return []
    return compute.search_clienti(store.clienti, q)


@app.get("/api/cliente/{ragione_sociale}")
def get_cliente(ragione_sociale: str) -> dict:
    if store.clienti is None:
        raise HTTPException(status_code=400, detail="Clienti non importati")

    scheda = compute.build_cliente_scheda(
        store.clienti,
        store.minord,
        store.ordini,
        ragione_sociale,
    )

    if scheda is None:
        raise HTTPException(status_code=404, detail="Cliente non trovato")

    return scheda
