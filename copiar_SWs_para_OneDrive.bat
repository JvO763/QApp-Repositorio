@echo off
rem ===========================================================================
rem  Copia os instaladores da pasta SWs\ (deste repositorio) para a pasta do QA
rem  no OneDrive: QApp-Dados\SWs\<SW>\. A partir do QApp 1.3.0 e de la que o
rem  time instala e atualiza os SWs (o GitHub nao e mais usado).
rem
rem  So copia o que falta ou o que for mais novo. Pode rodar quantas vezes quiser.
rem ===========================================================================
setlocal EnableExtensions
title Copiar SWs para o OneDrive
cd /d "%~dp0"

set "DADOS=%OneDriveCommercial%\QApp-Dados"
if "%OneDriveCommercial%"=="" set "DADOS="
if not exist "%DADOS%\qapp-dados.json" (
  echo  Nao encontrei a pasta QApp-Dados no OneDrive da empresa.
  set /p "DADOS=  Cole o caminho da pasta QApp-Dados: "
)
if not exist "%DADOS%\qapp-dados.json" goto :fail_dados
if not exist "%~dp0SWs" goto :fail_sws

echo.
echo  De:   %~dp0SWs
echo  Para: %DADOS%\SWs
echo.
robocopy "%~dp0SWs" "%DADOS%\SWs" *.exe *.msi /S /XO /R:2 /W:3 /NP /NJH /NDL
if errorlevel 8 goto :fail_copy
if not exist "%DADOS%\SWs\apps.json" if exist "%~dp0apps.json" copy /y "%~dp0apps.json" "%DADOS%\SWs\apps.json" >nul

echo.
echo  Pronto. O OneDrive vai enviar os arquivos para a nuvem (icone de nuvem na barra
echo  de tarefas). Depois disso o QApp 1.3.0 de todo o time ja enxerga os SWs.
echo.
start "" "%DADOS%\SWs"
pause
exit /b 0

:fail_dados
echo  ERRO: pasta QApp-Dados nao encontrada (precisa ter o arquivo qapp-dados.json).
goto :fail
:fail_sws
echo  ERRO: a pasta SWs nao existe ao lado deste arquivo.
goto :fail
:fail_copy
echo  ERRO: o robocopy nao conseguiu copiar (veja as mensagens acima).
:fail
echo.
pause
exit /b 1
