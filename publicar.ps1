<#
  Publica nos Releases do GitHub os instaladores da pasta SWs\ que ainda não foram publicados.
  O QApp de todo o time instala/atualiza sozinho em até 5 minutos.

  Estrutura esperada (a pasta SWs\ fica fora do Git, pelo .gitignore):
     SWs\ErroMalha\EagleAnaliseErro_Setup_1.3.0.exe
     SWs\ErroOclusao\EagleAnaliseOclusao_Setup_1.1.0.exe
     SWs\CalibracaoAutomatica\AutomacaoEDGE_Setup_1.6.0.exe
  Cada pasta corresponde ao campo "folder" do apps.json; a versão vem do nome do arquivo (…_1.3.0.exe).

  Requisitos: GitHub CLI (winget install --id GitHub.cli) — na primeira vez ele pede login.
  Uso (clique direito na pasta > Abrir no Terminal):
     powershell -ExecutionPolicy Bypass -File .\publicar.ps1             # publica o que faltar
     powershell -ExecutionPolicy Bypass -File .\publicar.ps1 -Simular    # só mostra o que faria
     powershell -ExecutionPolicy Bypass -File .\publicar.ps1 -PreRelease # publica como teste (o QApp ignora)
#>
param(
  [string]$Repo = 'JvO763/QApp-Repositorio',
  [switch]$Simular,
  [switch]$PreRelease
)
$ErrorActionPreference = 'Continue'
Set-Location $PSScriptRoot

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  Write-Host 'GitHub CLI não encontrado. Instale com:  winget install --id GitHub.cli  e abra um novo terminal.' -ForegroundColor Yellow
  exit 1
}
gh auth status *> $null
if ($LASTEXITCODE -ne 0) { gh auth login }

$apps = (Get-Content -Raw -Encoding UTF8 (Join-Path $PSScriptRoot 'apps.json') | ConvertFrom-Json).apps
$porPasta = @{}
foreach ($a in $apps) { if ($a.folder) { $porPasta[$a.folder.ToLower()] = $a } }

$existentes = @(gh release list --repo $Repo --limit 300 --json tagName --jq '.[].tagName' 2>$null)
$pastaSWs = Join-Path $PSScriptRoot 'SWs'
if (-not (Test-Path $pastaSWs)) { Write-Host "Pasta não encontrada: $pastaSWs" -ForegroundColor Red; exit 1 }

$publicados = 0
foreach ($dir in Get-ChildItem -Path $pastaSWs -Directory) {
  $app = $porPasta[$dir.Name.ToLower()]
  if (-not $app) {
    Write-Host "  ?   $($dir.Name): nenhuma entrada com ""folder"": ""$($dir.Name)"" no apps.json" -ForegroundColor Yellow
    continue
  }
  # instalador de maior versão da pasta
  $melhor = $null; $melhorVer = $null
  foreach ($f in Get-ChildItem -Path $dir.FullName -File | Where-Object { $_.Extension -in '.exe', '.msi' }) {
    if ($f.Name -match '(\d+(\.\d+){1,3})\.(exe|msi)$') {
      $v = [version]$Matches[1]
      if (-not $melhorVer -or $v -gt $melhorVer) { $melhor = $f; $melhorVer = $v }
    }
  }
  if (-not $melhor) { Write-Host "  --  $($app.name): nenhum instalador com versão no nome (ex.: Setup_1.2.0.exe)" -ForegroundColor DarkGray; continue }

  $ver = $melhorVer.ToString()
  $tag = "$($app.id)-v$ver"
  if ($existentes -contains $tag) { Write-Host "  ok  $tag já publicado" -ForegroundColor Green; continue }
  if ($Simular) { Write-Host "  >>  publicaria $tag  ($($melhor.Name), $([math]::Round($melhor.Length / 1MB)) MB)" -ForegroundColor Cyan; continue }

  Write-Host "  ... enviando $($melhor.Name) ($([math]::Round($melhor.Length / 1MB)) MB) como $tag" -ForegroundColor Cyan
  $extra = @()
  if ($PreRelease) { $extra += '--prerelease' }
  gh release create $tag $melhor.FullName --repo $Repo --title "$($app.name) $ver" --notes "Instalador $($melhor.Name)" @extra
  if ($LASTEXITCODE -eq 0) { Write-Host "  ok  $tag publicado" -ForegroundColor Green; $publicados++ }
  else { Write-Host "  erro ao publicar $tag" -ForegroundColor Red }
}
Write-Host ''
if ($publicados) { Write-Host "$publicados versão(ões) publicada(s). O QApp do time atualiza em até 5 minutos." -ForegroundColor Green }
else { Write-Host 'Nada novo para publicar.' }
Write-Host "Releases: https://github.com/$Repo/releases"
