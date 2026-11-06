# -*- coding: utf-8 -*-
"""
Aplica o visual do QApp no executável do MTF Automático SEM recompilar o programa.

O .exe é um PyInstaller "onefile": um carregador + um arquivo com o Python, as bibliotecas e o
script principal (bytecode). Este script troca só o script principal por um "envelope" que:
  1. aplica o tema do QApp no tkinter (qapp_tema_mtf.py) e
  2. executa o bytecode ORIGINAL do MTF, byte a byte igual ao de antes.
Bibliotecas, DLLs e o próprio cálculo continuam idênticos. Opcionalmente troca o ícone do .exe.

Precisa rodar com o MESMO Python do executável (3.12): o bytecode é específico da versão.
Uso: py -3.12 reempacotar_mtf.py ORIGINAL.exe SAIDA.exe --icone-png icone64.png [--carregador-com-icone X.exe]
     py -3.12 reempacotar_mtf.py ORIGINAL.exe - --extrair-carregador carregador.exe
"""
import argparse
import base64
import marshal
import struct
import sys
import zlib

MAGIC = b"MEI\014\013\012\013\016"
COOKIE = "!8sIIii64s"
ENTRY = "!IIIIBc"


def ler(exe):
    data = open(exe, "rb").read()
    pos = data.rfind(MAGIC)
    if pos < 0:
        raise SystemExit("Não é um executável do PyInstaller.")
    magic, pkglen, tocoff, toclen, pyver, pylib = struct.unpack(COOKIE, data[pos:pos + struct.calcsize(COOKIE)])
    inicio = len(data) - pkglen
    toc = data[inicio + tocoff:inicio + tocoff + toclen]
    entradas, i = [], 0
    while i < len(toc):
        es, off, clen, ulen, flag, typ = struct.unpack(ENTRY, toc[i:i + 18])
        nome = toc[i + 18:i + es].rstrip(b"\0")
        entradas.append(dict(nome=nome, flag=flag, typ=typ, ulen=ulen,
                             dados=data[inicio + off:inicio + off + clen]))
        i += es
    return data[:inicio], entradas, pyver, pylib


def gravar(saida, carregador, entradas, pyver, pylib):
    blob, toc = bytearray(), bytearray()
    for e in entradas:
        off = len(blob)
        blob += e["dados"]
        nome = e["nome"] + b"\0"
        es = struct.calcsize(ENTRY) + len(nome)
        es += (16 - es % 16) % 16                      # alinhamento usado pelo PyInstaller
        toc += struct.pack(ENTRY, es, off, len(e["dados"]), e["ulen"], e["flag"], e["typ"])
        toc += nome.ljust(es - struct.calcsize(ENTRY), b"\0")
    tocoff = len(blob)
    pkglen = len(blob) + len(toc) + struct.calcsize(COOKIE)
    cookie = struct.pack(COOKIE, MAGIC, pkglen, tocoff, len(toc), pyver, pylib)
    with open(saida, "wb") as f:
        f.write(carregador)
        f.write(blob)
        f.write(toc)
        f.write(cookie)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("original")
    ap.add_argument("saida")
    ap.add_argument("--tema", default="qapp_tema_mtf.py")
    ap.add_argument("--icone-png", default="")
    ap.add_argument("--carregador-com-icone", default="", help="carregador (parte .exe) já com o ícone novo")
    ap.add_argument("--extrair-carregador", default="", help="só grava o carregador (para trocar o ícone) e sai")
    a = ap.parse_args()

    carregador, entradas, pyver, pylib = ler(a.original)
    if a.extrair_carregador:
        open(a.extrair_carregador, "wb").write(carregador)
        print("ok", a.extrair_carregador)
        return
    if pyver != sys.version_info.major * 100 + sys.version_info.minor:
        raise SystemExit(f"Rode com o Python {pyver // 100}.{pyver % 100} (o do executável).")
    scripts = [e for e in entradas if e["typ"] == b"s" and not e["nome"].startswith((b"pyi_rth", b"pyiboot"))]
    if len(scripts) != 1:
        raise SystemExit(f"Esperava 1 script principal, achei {[e['nome'] for e in scripts]}")
    main_e = scripts[0]
    original = zlib.decompress(main_e["dados"]) if main_e["flag"] else main_e["dados"]
    marshal.loads(original)                            # confere que é bytecode desta versão
    if b"QAPP_TEMA_MTF" in original:
        raise SystemExit("Este executável já está com o visual do QApp.")

    tema = open(a.tema, encoding="utf-8").read()
    if a.icone_png:
        tema = tema.replace('"__ICONE__"', repr(base64.b64encode(open(a.icone_png, "rb").read()).decode()), 1)
    envelope = (
        "# QAPP_TEMA_MTF: visual do QApp + programa original sem alteração\n"
        f"_QAPP_TEMA = {tema!r}\n"
        f"_QAPP_ORIGINAL = {original!r}\n"
        "try:\n"
        "    exec(compile(_QAPP_TEMA, 'qapp_tema_mtf.py', 'exec'), {'__name__': 'qapp_tema_mtf'})\n"
        "except Exception:\n"
        "    pass\n"
        "import marshal as _qapp_marshal\n"
        "_qapp_codigo = _qapp_marshal.loads(_QAPP_ORIGINAL)\n"
        "del _QAPP_TEMA, _QAPP_ORIGINAL, _qapp_marshal\n"
        "exec(_qapp_codigo, globals())\n"
    )
    nome_arquivo = marshal.loads(original).co_filename
    codigo = compile(envelope, nome_arquivo, "exec")
    novo = marshal.dumps(codigo)
    main_e["dados"] = zlib.compress(novo, 9)
    main_e["flag"] = 1
    main_e["ulen"] = len(novo)

    if a.carregador_com_icone:
        carregador = open(a.carregador_com_icone, "rb").read()
    gravar(a.saida, carregador, entradas, pyver, pylib)
    print("ok", a.saida)


if __name__ == "__main__":
    main()
