# -*- coding: utf-8 -*-
"""
Visual do QApp para o MTF Automático (POSITION_EVALUATION).

Roda ANTES do programa original e só muda a aparência: tema escuro do QApp nos widgets
ttk/tk, barra de título escura e o ícone do QApp. O código do MTF (cálculos, leitura das
imagens, relatórios PDF/CSV) é executado sem nenhuma alteração logo depois.
"""
import base64 as _b64
import os as _os
import tkinter as _tk
from tkinter import ttk as _ttk

Q = {
    "bg": "#0a0f1e", "panel": "#10162c", "field": "#131a35", "line": "#2a3457",
    "text": "#e9edff", "muted": "#8f9abf", "dim": "#5d6890",
    "brand": "#a5b4fc", "brand_hover": "#c7d2fe", "ink": "#0b1020",
    "sec": "#1b2447", "sec_hover": "#2a3457", "accent": "#a78bfa",
}
FONTE = "Segoe UI"
ICONE_PNG_B64 = "__ICONE__"   # trocado pelo empacotador (PNG 64x64 do ícone do QApp)

_icone = {}


def _barra_escura(janela):
    """Barra de título escura (Windows 10 2004+ / 11)."""
    if _os.name != "nt":
        return
    try:
        import ctypes
        janela.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(janela.winfo_id()) or janela.winfo_id()
        v = ctypes.c_int(1)
        for attr in (20, 19):
            if ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(v), ctypes.sizeof(v)) == 0:
                break
    except Exception:
        pass


def _estilo(root):
    c = Q
    root.configure(bg=c["bg"])
    # widgets clássicos do tk (Listbox, Menu, Canvas, Toplevel...)
    for chave, valor in (
        ("*Background", c["bg"]), ("*Foreground", c["text"]), ("*Font", (FONTE, 10)),
        ("*activeBackground", c["sec_hover"]), ("*activeForeground", c["text"]),
        ("*selectBackground", c["brand"]), ("*selectForeground", c["ink"]),
        ("*insertBackground", c["text"]), ("*highlightThickness", 0),
        ("*disabledForeground", c["dim"]), ("*troughColor", c["field"]),
        ("*Listbox.background", c["field"]), ("*Listbox.relief", "flat"), ("*Listbox.borderWidth", 0),
        ("*Menu.background", c["panel"]), ("*Menu.activeBackground", c["sec_hover"]),
        ("*Menu.relief", "flat"), ("*Menu.borderWidth", 1),
        ("*Entry.background", c["field"]), ("*Text.background", c["field"]),
        ("*TCombobox*Listbox.background", c["panel"]), ("*TCombobox*Listbox.foreground", c["text"]),
        ("*TCombobox*Listbox.selectBackground", c["brand"]), ("*TCombobox*Listbox.selectForeground", c["ink"]),
        ("*TCombobox*Listbox.font", (FONTE, 10)),
    ):
        root.option_add(chave, valor)

    s = _ttk.Style(root)
    try:
        s.theme_use("clam")
    except Exception:
        pass
    s.configure(".", background=c["bg"], foreground=c["text"], fieldbackground=c["field"],
                bordercolor=c["line"], darkcolor=c["bg"], lightcolor=c["bg"], troughcolor=c["field"],
                focuscolor=c["brand"], selectbackground=c["brand"], selectforeground=c["ink"],
                insertcolor=c["text"], arrowcolor=c["text"], font=(FONTE, 10))
    s.map(".", foreground=[("disabled", c["dim"])])
    s.configure("TFrame", background=c["bg"])
    s.configure("TLabel", background=c["bg"], foreground=c["text"])
    s.configure("TButton", background=c["sec"], foreground=c["text"], bordercolor=c["line"],
                lightcolor=c["sec"], darkcolor=c["sec"], relief="flat", padding=(12, 5),
                font=(FONTE, 10, "bold"))
    s.map("TButton",
          background=[("disabled", c["panel"]), ("pressed", c["brand"]), ("active", c["sec_hover"])],
          foreground=[("disabled", c["dim"]), ("pressed", c["ink"])],
          lightcolor=[("pressed", c["brand"]), ("active", c["sec_hover"])],
          darkcolor=[("pressed", c["brand"]), ("active", c["sec_hover"])],
          bordercolor=[("focus", c["brand"])])
    for w in ("TEntry", "TSpinbox"):
        s.configure(w, fieldbackground=c["field"], foreground=c["text"], bordercolor=c["line"],
                    lightcolor=c["field"], darkcolor=c["field"], insertcolor=c["text"], padding=4,
                    background=c["sec"], arrowcolor=c["text"])
        s.map(w, bordercolor=[("focus", c["brand"])], lightcolor=[("focus", c["brand"])],
              fieldbackground=[("disabled", c["panel"])])
    s.configure("TCombobox", fieldbackground=c["field"], background=c["sec"], foreground=c["text"],
                arrowcolor=c["text"], bordercolor=c["line"], lightcolor=c["field"], darkcolor=c["field"], padding=4)
    s.map("TCombobox", fieldbackground=[("readonly", c["field"]), ("disabled", c["panel"])],
          foreground=[("readonly", c["text"])], selectbackground=[("readonly", c["field"])],
          selectforeground=[("readonly", c["text"])], background=[("active", c["sec_hover"])],
          bordercolor=[("focus", c["brand"])])
    for w in ("TCheckbutton", "TRadiobutton"):
        s.configure(w, background=c["bg"], foreground=c["text"], indicatorbackground=c["field"],
                    indicatorforeground=c["ink"], upperbordercolor=c["line"], lowerbordercolor=c["line"],
                    indicatormargin=(0, 0, 6, 0))
        s.map(w, background=[("active", c["bg"])],
              indicatorbackground=[("selected", c["brand"]), ("active", c["sec_hover"])])
    s.configure("Horizontal.TProgressbar", background=c["brand"], troughcolor=c["field"],
                bordercolor=c["line"], lightcolor=c["brand"], darkcolor=c["brand"])
    s.configure("Vertical.TProgressbar", background=c["brand"], troughcolor=c["field"],
                bordercolor=c["line"], lightcolor=c["brand"], darkcolor=c["brand"])
    for w in ("Horizontal.TScale", "Vertical.TScale", "TScale"):
        s.configure(w, background=c["brand"], troughcolor=c["field"], bordercolor=c["line"],
                    lightcolor=c["brand"], darkcolor=c["brand"])
    s.configure("TLabelframe", background=c["bg"], bordercolor=c["line"], lightcolor=c["bg"], darkcolor=c["bg"])
    s.configure("TLabelframe.Label", background=c["bg"], foreground=c["muted"], font=(FONTE, 9, "bold"))
    s.configure("TNotebook", background=c["bg"], bordercolor=c["line"], lightcolor=c["bg"], darkcolor=c["bg"])
    s.configure("TNotebook.Tab", background=c["bg"], foreground=c["muted"], bordercolor=c["line"],
                lightcolor=c["bg"], darkcolor=c["bg"], padding=(14, 6), font=(FONTE, 10, "bold"))
    s.map("TNotebook.Tab", background=[("selected", c["sec"])], foreground=[("selected", c["text"])],
          lightcolor=[("selected", c["sec"])])
    s.configure("Treeview", background=c["panel"], fieldbackground=c["panel"], foreground=c["text"],
                bordercolor=c["line"], rowheight=24)
    s.map("Treeview", background=[("selected", c["brand"])], foreground=[("selected", c["ink"])])
    s.configure("Treeview.Heading", background=c["field"], foreground=c["muted"], bordercolor=c["line"],
                lightcolor=c["field"], darkcolor=c["field"], font=(FONTE, 9, "bold"))
    for w in ("Vertical.TScrollbar", "Horizontal.TScrollbar"):
        s.configure(w, background=c["sec"], troughcolor=c["bg"], bordercolor=c["bg"], arrowcolor=c["muted"],
                    lightcolor=c["sec"], darkcolor=c["sec"], gripcount=0)
        s.map(w, background=[("active", c["sec_hover"])])
    s.configure("TSeparator", background=c["line"])
    s.configure("TPanedwindow", background=c["bg"])

    try:
        if ICONE_PNG_B64 and ICONE_PNG_B64 != "__ICONE__":
            _icone["img"] = _tk.PhotoImage(master=root, data=ICONE_PNG_B64)
            root.iconphoto(True, _icone["img"])   # vale para todas as janelas
    except Exception:
        pass
    root.after_idle(lambda: _barra_escura(root))
    try:
        _instalar_graficos()
    except Exception:
        pass


_tk_init = _tk.Tk.__init__
_top_init = _tk.Toplevel.__init__


def _novo_tk_init(self, *a, **k):
    _tk_init(self, *a, **k)
    try:
        _estilo(self)
    except Exception:
        pass


def _novo_top_init(self, *a, **k):
    _top_init(self, *a, **k)
    try:
        self.configure(bg=Q["bg"])
        self.after_idle(lambda: _barra_escura(self))
    except Exception:
        pass


_tk.Tk.__init__ = _novo_tk_init
_tk.Toplevel.__init__ = _novo_top_init


# ---------------------------------------------------------------- gráficos na janela
# Os gráficos que aparecem NA JANELA (FigureCanvasTkAgg) ficam no tema escuro. Ao salvar
# (PNG/PDF/relatório) as cores originais voltam durante o salvamento: arquivos e relatórios
# saem exatamente como antes.

def _lum(c):
    try:
        from matplotlib.colors import to_rgba
        r, g, b, a = to_rgba(c)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b, a
    except Exception:
        return None, 0


def _quase_preto(c):
    """Preto/cinza bem escuro (texto e eixos padrão). Cores de dados (vermelho, azul...) não."""
    try:
        from matplotlib.colors import to_rgba
        r, g, b, a = to_rgba(c)
        return a > 0 and max(r, g, b) < 0.3
    except Exception:
        return False


def _restaurar(fig):
    for setter, original, _novo in reversed(getattr(fig, "_qapp_mudancas", [])):
        try:
            setter(original)
        except Exception:
            pass
    fig._qapp_mudancas = []


def _escurecer(fig):
    import matplotlib.lines as mlines
    import matplotlib.patches as mpatches
    import matplotlib.text as mtext
    _restaurar(fig)
    mud = []

    def troca(setter, original, novo):
        mud.append((setter, original, novo))
        setter(novo)

    troca(fig.patch.set_facecolor, fig.patch.get_facecolor(), Q["bg"])
    eixos_patches = set()
    grades = set()
    for ax in fig.axes:
        eixos_patches.add(ax.patch)
        l, a = _lum(ax.get_facecolor())
        if l is not None and a > 0 and l > 0.8:
            troca(ax.set_facecolor, ax.get_facecolor(), Q["panel"])
        for sp in ax.spines.values():
            if _quase_preto(sp.get_edgecolor()):
                troca(sp.set_edgecolor, sp.get_edgecolor(), "#5d6890")
        for eixo in (ax.xaxis, ax.yaxis):
            for t in eixo.get_major_ticks() + eixo.get_minor_ticks():
                grades.add(t.gridline)
    for ln in fig.findobj(mlines.Line2D):
        cor = ln.get_color()
        l, a = _lum(cor)
        if l is None:
            continue
        if ln in grades:
            troca(ln.set_color, cor, "#2a3457")
        elif _quase_preto(cor):
            troca(ln.set_color, cor, "#c5ccEB")
    for t in fig.findobj(mtext.Text):
        if _quase_preto(t.get_color()):
            troca(t.set_color, t.get_color(), Q["text"])
        caixa = t.get_bbox_patch()
        if caixa is not None:
            l, a = _lum(caixa.get_facecolor())
            if l is not None and a > 0 and l > 0.8:
                troca(caixa.set_facecolor, caixa.get_facecolor(), Q["field"])
                troca(caixa.set_edgecolor, caixa.get_edgecolor(), Q["line"])
    for p in fig.findobj(mpatches.Patch):
        if p is fig.patch or p in eixos_patches:
            continue
        l, a = _lum(p.get_facecolor())
        if l is not None and a > 0 and l > 0.9:
            troca(p.set_facecolor, p.get_facecolor(), Q["field"])
            le, ae = _lum(p.get_edgecolor())
            if le is not None and ae > 0 and le > 0.6:
                troca(p.set_edgecolor, p.get_edgecolor(), Q["line"])
    fig._qapp_mudancas = mud


def _instalar_graficos():
    import sys
    mod = sys.modules.get("matplotlib.backends.backend_tkagg")
    if mod is None:
        import matplotlib.backends.backend_tkagg as mod   # o MTF usa este mesmo backend
    if getattr(mod.FigureCanvasTkAgg, "_qapp", False):
        return
    from matplotlib.figure import Figure
    desenhar = mod.FigureCanvasTkAgg.draw
    salvar = Figure.savefig

    def draw(self, *a, **k):
        try:
            _escurecer(self.figure)
        except Exception:
            pass
        return desenhar(self, *a, **k)

    def savefig(self, *a, **k):
        if not getattr(self, "_qapp_mudancas", None):
            return salvar(self, *a, **k)
        mud = list(self._qapp_mudancas)
        _restaurar(self)                     # salva com as cores originais
        try:
            return salvar(self, *a, **k)
        finally:
            for setter, _orig, novo in mud:
                try:
                    setter(novo)
                except Exception:
                    pass
            self._qapp_mudancas = mud

    mod.FigureCanvasTkAgg.draw = draw
    mod.FigureCanvasTkAgg._qapp = True
    Figure.savefig = savefig
