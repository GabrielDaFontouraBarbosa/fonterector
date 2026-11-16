@echo off
rem Abre o tunel publico do jogo (Cloudflare) e reabre sozinho se cair.
rem O endereco e a linha https://....trycloudflare.com. Ele so muda se este script for reiniciado.
:de_novo
"%~dp0cloudflared\cloudflared.exe" tunnel --no-autoupdate --url http://127.0.0.1:8777
echo.
echo Tunel caiu. Reconectando em 3 segundos...
timeout /t 3 /nobreak >nul
goto de_novo
