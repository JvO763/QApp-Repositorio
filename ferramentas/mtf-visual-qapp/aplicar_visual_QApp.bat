@echo off
rem ===========================================================================
rem  Aplica o visual do QApp num executavel do MTF Automatico (POSITION_EVALUATION)
rem  e publica na pasta do QA no OneDrive (QApp-Dados\SWs\MTFAutomatico\).
rem
rem  NAO recompila o MTF: o calculo, as bibliotecas e os relatorios ficam identicos.
rem  Troca so a aparencia (tema escuro do QApp) e o icone do .exe.
rem
rem  Uso: arraste o .exe NOVO do MTF (sem o visual) para cima deste arquivo.
rem       Sem arrastar, usa o .exe mais recente de QApp-Repositorio\SWs\MTFAutomatico.
rem  Precisa do Python 3.12 (o mesmo do executavel): winget install Python.Python.3.12
rem ===========================================================================
setlocal EnableExtensions
title Visual do QApp no MTF
cd /d "%~dp0"

set "ORIG=%~1"
if not defined ORIG for /f "delims=" %%F in ('dir /b /a-d /o-d "%~dp0..\..\SWs\MTFAutomatico\*.exe" 2^>nul') do if not defined ORIG set "ORIG=%~dp0..\..\SWs\MTFAutomatico\%%F"
if not defined ORIG goto :sem_exe
if not exist "%ORIG%" goto :sem_exe
for %%F in ("%ORIG%") do set "NOME=%%~nxF"
echo  Executavel: %ORIG%

py -3.12 -c "import sys" >nul 2>&1
if errorlevel 1 goto :sem_python

set "DADOS="
if defined QAPP_DADOS if exist "%QAPP_DADOS%\qapp-dados.json" set "DADOS=%QAPP_DADOS%"
if not defined DADOS if defined OneDriveCommercial if exist "%OneDriveCommercial%\QApp-Dados\qapp-dados.json" set "DADOS=%OneDriveCommercial%\QApp-Dados"
if not defined DADOS goto :sem_pasta

set "TMPD=%TEMP%\qapp_mtf_visual"
if exist "%TMPD%" rmdir /s /q "%TMPD%"
mkdir "%TMPD%"

rem icone do .exe (opcional): usa o rcedit que o gerador do QApp ja baixou
set "CARREG="
set "RCEDIT=%LOCALAPPDATA%\electron-builder\Cache\winCodeSign\winCodeSign-2.6.0\rcedit-x64.exe"
if not exist "%RCEDIT%" goto :sem_icone
py -3.12 reempacotar_mtf.py "%ORIG%" - --extrair-carregador "%TMPD%\carregador.exe" >nul
if errorlevel 1 goto :sem_icone
"%RCEDIT%" "%TMPD%\carregador.exe" --set-icon "%~dp0icone_mtf.ico"
if errorlevel 1 goto :sem_icone
set "CARREG=--carregador-com-icone "%TMPD%\carregador.exe""
goto :montar
:sem_icone
echo  (sem o rcedit: o .exe fica com o icone antigo; a janela ja usa o icone do QApp)

:montar
if not exist "%DADOS%\SWs\MTFAutomatico" mkdir "%DADOS%\SWs\MTFAutomatico"
py -3.12 reempacotar_mtf.py "%ORIG%" "%TMPD%\%NOME%" --tema "%~dp0qapp_tema_mtf.py" --icone-png "%~dp0icone_mtf_64.png" %CARREG%
if errorlevel 1 goto :falhou
copy /y "%TMPD%\%NOME%" "%DADOS%\SWs\MTFAutomatico\%NOME%" >nul
if errorlevel 1 goto :falhou
rmdir /s /q "%TMPD%" >nul 2>&1
echo.
echo  [OneDrive] publicado: QApp-Dados\SWs\MTFAutomatico\%NOME%
echo  O QApp do time atualiza sozinho (a versao vem do nome: ..._V2_4_... = 2.4).
echo.
pause
exit /b 0

:sem_exe
echo  ERRO: nenhum .exe do MTF encontrado. Arraste o .exe para cima deste arquivo.
goto :fim
:sem_python
echo  ERRO: Python 3.12 nao encontrado (precisa ser o mesmo do executavel).
echo        Instale com:  winget install Python.Python.3.12
goto :fim
:sem_pasta
echo  ERRO: pasta QApp-Dados nao encontrada (defina QAPP_DADOS com o caminho).
goto :fim
:falhou
echo  ERRO: nao consegui aplicar o visual (veja a mensagem acima).
:fim
echo.
pause
exit /b 1
