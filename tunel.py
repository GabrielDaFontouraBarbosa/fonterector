"""Abre o túnel Cloudflare do jogo e publica o endereço dele no link fixo.

O endereço do túnel (https://….trycloudflare.com) muda toda vez que ele reconecta.
Este script, a cada endereço novo, grava docs/link.txt e manda pro GitHub; a página
https://gabrieldafontourabarbosa.github.io/fonterector/ lê esse arquivo e redireciona.
Então o link que você passa pros amigos é sempre o mesmo.

Rodar (com o servidor.py já rodando):  python tunel.py
"""
import pathlib
import re
import subprocess
import sys
import time

AQUI = pathlib.Path(__file__).parent
EXE = AQUI / "cloudflared" / "cloudflared.exe"
LINK = AQUI / "docs" / "link.txt"
PORTA = sys.argv[1] if len(sys.argv) > 1 else "8777"


def publicar(url: str):
    LINK.write_text(url + "\n", encoding="utf-8")
    git = ["git", "-C", str(AQUI)]
    subprocess.run(git + ["add", str(LINK)], check=False)
    feito = subprocess.run(git + ["commit", "-m", "Atualiza o link do túnel", "--", str(LINK)], capture_output=True)
    if feito.returncode == 0:
        r = subprocess.run(git + ["push", "-q"], capture_output=True, text=True)
        print("  link fixo atualizado" if r.returncode == 0 else "  ERRO no push: " + r.stderr.strip(), flush=True)


def main():
    if not EXE.exists():
        sys.exit(f"Falta o cloudflared em {EXE} — baixe em github.com/cloudflare/cloudflared/releases")
    while True:
        proc = subprocess.Popen([str(EXE), "tunnel", "--no-autoupdate", "--url", f"http://127.0.0.1:{PORTA}"],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        for linha in proc.stdout:
            achou = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", linha)
            if achou:
                print(f"\n  Túnel: {achou.group(0)}\n  Link fixo: https://gabrieldafontourabarbosa.github.io/fonterector/\n", flush=True)
                publicar(achou.group(0))
            elif " ERR " in linha:
                print(linha.rstrip(), flush=True)
        print("Túnel caiu. Reconectando em 3 segundos...", flush=True)
        time.sleep(3)


if __name__ == "__main__":
    main()
