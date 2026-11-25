# Fonterector The Game

Jogo do Gabriel com os amigos. Tudo em português (código, comentários, textos do jogo).

## Como está montado

- `index.html` é o jogo inteiro: um `<script>` só, dividido em seções `// ───────── Nome ─────────`. Sem build.
- `servidor.py` só repassa mensagens. Toda regra de jogo roda no navegador.
- Quem decide um acerto é quem atirou; quem leva o tiro aplica o dano. Bots, zumbis e ondas são simulados pelo **host** (menor id da sala).
- Bots têm id negativo (-1 a -9); zumbis, -10 pra baixo.
- O PC da Safe House (mini VS Code) baixa Skulpt (Python) e Fengari (Lua) do jsDelivr só quando alguém roda código, dentro de um Worker. Java é traduzido pra JS na hora (`javaParaJs`).
- Modelos chegam depois da página. Se um não carregar, o jogo cai nas versões de caixa (`criarModeloCaixas`, `animarCaixas`, armas de caixinha), então nada quebra sem os assets.

## Testar

- `fonterector-teste` no `.claude/launch.json` sobe uma sala separada na porta 8778, pra não derrubar quem está jogando na 8777.
- O navegador de teste do app roda a poucos quadros por segundo e com animações reduzidas: teste a lógica chamando as funções pelo console, não pela sensação de jogo.

## Cuidados

- O repositório é **público**. `victor.jpg` (foto de uma pessoa real) e `cloudflared/` ficam fora do git de propósito.
- A senha da classe Fonterector está no código da página. É trava de brincadeira, não segurança.
- Assets novos: só CC0 ou com licença que permita, com o `License.txt` junto na pasta.
