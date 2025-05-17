@echo off
setlocal

:: Configurações
set RENDER_API_KEY=rnd_UhBwDoaYgme11gIhZlGVlfevdBKw
set RENDER_SERVICE_ID=srv-d0k91cd6ubrc73b36ne0

:: 1️⃣ Commit e Push no GitHub
echo 🔄 Enviando atualizações para o GitHub...
git add .
git commit -m "🚀 Atualização automática via script"
git push --force

:: 2️⃣ Deploy na Render via API
echo 🔄 Iniciando Deploy na Render...
curl -X POST "https://api.render.com/v1/services/%RENDER_SERVICE_ID%/deploys" ^
 -H "Authorization: Bearer %RENDER_API_KEY%" ^
 -H "Content-Type: application/json" ^
 -d "{}"

echo ✅ Deploy concluído! Acesse: https://dashboard.render.com/web/%RENDER_SERVICE_ID%

endlocal
pause
