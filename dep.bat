@echo off
echo 🚀 Iniciando Deploy...

:: Atualiza o .gitignore e remove arquivos indesejados do controle do Git
git rm --cached -r *.json >nul 2>&1
git add .
git commit -m "🚀 Atualização automática via script"
git push --force

:: Faz o deploy automático no Render via API
curl -X POST https://api.render.com/v1/services/srv-d0k91cd6ubrc73b36ne0/deploys \
  -H "Accept: application/json" \
  -H "Authorization: Bearer rnd_UhBwDoaYgme11gIhZlGVlfevdBKw" \
  -d ""

echo ✅ Deploy concluído! Acesse: https://dashboard.render.com/web/srv-d0k91cd6ubrc73b36ne0
pause
