"""Fonterector The Game — servidor relay. Só repassa mensagens entre os jogadores da mesma sala.

Rodar:  python arena-pvp/servidor.py   →  http://<seu-ip>:8777
"""
import itertools
import json
import pathlib
import socket
import sys

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

AQUI = pathlib.Path(__file__).parent
PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 8777   # porta opcional: python servidor.py 8778
MAX_JOGADORES = 5      # por sala

app = FastAPI()
salas: dict[str, dict[int, WebSocket]] = {}    # código da sala -> {id do jogador: conexão}
ids = itertools.count(1)


@app.get("/")
def index():
    return FileResponse(AQUI / "index.html", headers={"Cache-Control": "no-store"})


@app.get("/victor.jpg")
def victor():
    """Foto opcional pro rosto da classe Victor Gomes (arena-pvp/victor.jpg)."""
    foto = AQUI / "victor.jpg"
    if not foto.exists():
        raise HTTPException(404)
    return FileResponse(foto)


if (AQUI / "assets").is_dir():      # modelos de armas e cenário (ver assets/*/License.txt)
    app.mount("/assets", StaticFiles(directory=AQUI / "assets"), name="assets")


async def repassar(sala: dict[int, WebSocket], de: int, texto: str):
    for i, c in list(sala.items()):
        if i != de:
            try:
                await c.send_text(texto)
            except Exception:
                sala.pop(i, None)


@app.websocket("/ws")
async def ws(sock: WebSocket):
    await sock.accept()
    codigo = "".join(ch for ch in (sock.query_params.get("sala") or "GERAL").upper() if ch.isalnum())[:8] or "GERAL"
    sala = salas.setdefault(codigo, {})
    if len(sala) >= MAX_JOGADORES:
        await sock.send_text(json.dumps({"t": "cheio"}))
        await sock.close()
        return
    meu = next(ids)
    sala[meu] = sock
    await sock.send_text(json.dumps({"t": "oi", "id": meu}))
    try:
        while True:
            msg = await sock.receive_text()
            if msg.startswith("{") and len(msg) < 2000:
                # carimba quem mandou: {"t":...} -> {"id":N,"t":...}
                await repassar(sala, meu, '{"id":%d,%s' % (meu, msg[1:]))
    except Exception:
        pass  # jogador saiu, ou a conexão já tinha caído quando outro tentou mandar pra ela
    finally:
        sala.pop(meu, None)
        if not sala and salas.get(codigo) is sala:
            salas.pop(codigo, None)      # sala vazia some
        await repassar(sala, meu, json.dumps({"id": meu, "t": "saiu"}))


def ip_local() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    print(f"\n  Fonterector The Game -> mande pro amigo: http://{ip_local()}:{PORTA}\n")
    uvicorn.run(app, host="0.0.0.0", port=PORTA, log_level="warning")
