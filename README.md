# Fonterector The Game

Jogo de tiro em primeira pessoa, multiplayer, que roda no navegador. Low poly, até 5 jogadores por sala.

**Ato 5 — Victor Gomes morre de novo.**

## Rodar

```bash
pip install -r requirements.txt
python servidor.py
```

Abre em `http://localhost:8777`. Na mesma rede Wi‑Fi, os outros entram pelo IP que o servidor imprime.

### Jogar com quem está longe

Precisa do [cloudflared](https://github.com/cloudflare/cloudflared/releases/latest) (`cloudflared-windows-amd64.exe`) salvo como `cloudflared/cloudflared.exe`. Com o servidor rodando, em outro terminal:

```bash
python tunel.py
```

**Link fixo pros amigos: https://gabrieldafontourabarbosa.github.io/fonterector/**

O túnel ganha um endereço novo toda vez que reconecta. O `tunel.py` grava o endereço atual em `docs/link.txt` e manda pro GitHub; a página do link fixo lê esse arquivo e redireciona. Leva até um minuto pra atualizar depois que o túnel sobe.

## Modos

- **Arcade** — todos contra todos, primeiro a 10 abates vence. `B` / `N` chamam e tiram bots.
- **Defender o Fonterector** — todos juntos contra ondas de zumbis que atacam o obelisco do centro.
- **Safe House** — lobby: casa, praça com fonte, árvores. Sem dano, pra ficar de boa.

Criar sala gera um link `?sala=XXXX`; quem abrir esse link cai na mesma partida.

## Classes

| Classe | Vida | Arma | Skill (`F`) |
|---|---|---|---|
| Brutus | 150 | primária + secundária | Escudo: 60% menos dano por 4 s |
| Recruta | 100 | primária + secundária | Adrenalina: cura 60 e corre mais |
| Sombra | 75 | primária + secundária | Salto sombrio: teleporta 9 m |
| Victor Gomes | 110 | katana em combo de 3, com dash | Corte giratório |
| Fonterector 🔒 | 140 | mísseis teleguiados (senha no loadout) | Salva de 5 mísseis |
| Felipe Smite Lime | 115 | raio em cadeia (Zeus) | Fúria de Zeus: chuva de raios |

## Controles

`WASD` anda · `Shift` corre · `Espaço` pula · `C` agacha · clique atira · botão direito mira · `R` recarrega · `F` skill · `C` correndo desliza · `1` `2` `Q` troca de arma · `L` loadout · `Esc` menu · `T` `G` `H` emotes

## Arquivos

- `index.html` — o jogo inteiro (three.js r128 via CDN)
- `servidor.py` — servidor FastAPI: entrega a página e repassa as mensagens entre os jogadores de cada sala
- `assets/` — modelos 3D CC0 (licenças em cada pasta) e `assets/amigo/PulseRifle.glb`, feito por um amigo do Gabriel
- `tunel.py` e `docs/` — túnel público e a página do link fixo
- `victor.jpg` — opcional, fora do git: foto pintada na cabeça do Victor Gomes. Sem ela aparece um rosto desenhado.

## Créditos

- Armas: [Ultimate Gun Pack](https://opengameart.org/content/low-poly-guns-pack), Quaternius (CC0)
- Boneco e animações: [Universal Animation Library](https://quaternius.com/packs/universalanimationlibrary.html), Quaternius (CC0)
- Cenário: [City Kit Industrial](https://kenney.nl/assets/city-kit-industrial), Kenney (CC0)
- Míssil: [Blaster Kit](https://kenney.nl/assets/blaster-kit), Kenney (CC0)
