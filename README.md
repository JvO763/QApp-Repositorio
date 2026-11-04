# QApp — links e instaladores do QA

Este repositório alimenta o **QApp** de todo o time:

| O quê | Onde | Chega no QApp em |
|---|---|---|
| Links do time | `links.json` (commit) | até 1 minuto |
| Lista de SW (nome, grupo, ícone, como instalar/abrir) | `apps.json` (commit) | até 1 minuto |
| Instaladores | **Releases** (um por versão) | até 5 minutos — instala/atualiza sozinho |

> Os instaladores ficam na pasta `SWs\` deste clone, mas **não vão para o Git** (estão no `.gitignore`):
> o GitHub recusa arquivos acima de 100 MB e o histórico ficaria enorme. Eles são publicados nos **Releases**.

## Publicar uma versão nova de um SW

1. Coloque o instalador novo na pasta do SW, com a versão no nome:
   `SWs\ErroMalha\EagleAnaliseErro_Setup_1.3.0.exe` (também vale `..._V2_4_...exe`)
2. Rode o script (clique direito na pasta do repositório → *Abrir no Terminal*):
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\publicar.ps1
   ```
   Ele publica um release para cada instalador que ainda não foi publicado (tag `erro-malha-v1.3.0`).
   Use `-Simular` para só ver o que faria, ou `-PreRelease` para testar sem o time receber.

Precisa do GitHub CLI uma vez: `winget install --id GitHub.cli` (na primeira execução ele pede login).

**Sem o script, pelo site:** *Releases → Draft a new release* → em *Choose a tag* digite `erro-malha-v1.3.0`
→ *Create new tag* → título livre → arraste o `.exe` → **Publish release**.

| Pasta em `SWs\` | id (começo da tag) |
|---|---|
| `ErroMalha` | `erro-malha` |
| `ErroOclusao` | `erro-oclusao` |
| `CalibracaoAutomatica` | `calibracao-automatica` |
| `MTFAutomatico` | `mtf-automatico` (portátil: o `.exe` roda sem instalar) |

## Adicionar um SW novo

1. Copie uma entrada do `apps.json`, troque `id`, `folder`, `name`, `group`… e faça commit + push.
2. Crie a pasta `SWs\<folder>`, coloque o instalador e rode `publicar.ps1`.

| Campo | Para quê |
|---|---|
| `id` | Identificador; começo da tag dos releases |
| `folder` | Pasta dentro de `SWs\` (usada pelo `publicar.ps1`) |
| `name`, `description`, `group`, `iconKey`, `order` | Como aparece no QApp (`iconKey`: mesh, occlusion, calibration, mtf, scan, tool) |
| `silentArgs` | Instalação sem cliques. NSIS: `/S` · Inno Setup: `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-` · `.msi` não precisa |
| `uninstallKey` | Chave em `...\CurrentVersion\Uninstall` do registro — o QApp lê dali a versão instalada |
| `exe` | Executável dentro da pasta de instalação (para abrir o app) |
| `installedPath` | Caminho completo do executável (alternativa ao registro; aceita `%LOCALAPPDATA%`, `%ProgramFiles%` e lista) |
| `requiresAdmin` | `true` pede UAC direto |

## Links do time

Adicione/edite pelo próprio QApp (botão **+** ou clique direito num link): cada alteração vira um commit aqui,
com o nome de quem alterou. Se editar `links.json` à mão, faça *Fetch/Pull* antes no GitHub Desktop.

## Token do QApp

Para o QApp gravar links: <https://github.com/settings/personal-access-tokens/new>
- *Repository access:* **Only select repositories** → `QApp-Repositorio`
- *Permissions → Contents:* **Read and write**
- Defina a validade e anote para renovar. Nunca faça commit do token.
