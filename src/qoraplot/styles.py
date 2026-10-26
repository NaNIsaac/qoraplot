"""rcParams for each variant and context.

`box` is the Origin-like look: a closed frame with ticks inside on all four sides, minor ticks and
no grid. `house` follows the figures already in the owner's repositories: an open L frame, grey
axes, near-black text, a light grid and IBM Plex Sans with STIX math.
"""

from importlib import resources
from typing import Literal

import cvdkit
from matplotlib import font_manager

type Variant = Literal["box", "house"]
type Context = Literal["paper", "poster", "slide"]
VARIANTS: tuple[Variant, ...] = ("box", "house")
CONTEXTS: tuple[Context, ...] = ("paper", "poster", "slide")

INK, INK_SOFT, GRID = "#0b0b0b", "#52514e", "#e4e3df"
SANS = ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"]
PLEX = "IBM Plex Sans"

# font size, small font size, line width, marker size, frame width, major and minor tick length.
# The poster row is the scale of the existing A0 poster figures.
_SCALE: dict[Context, tuple[float, ...]] = {
    "paper": (8, 7, 1.2, 4, 0.8, 3.5, 2.0),
    "slide": (16, 14, 2.2, 7, 1.2, 5.0, 3.0),
    "poster": (26, 23, 3.2, 10, 1.4, 7.0, 4.0),
}

_fonts_added = False


def _add_fonts() -> None:
    global _fonts_added
    if _fonts_added:
        return
    for ttf in resources.files("qoraplot").joinpath("fonts").iterdir():
        if ttf.name.endswith(".ttf"):
            with resources.as_file(ttf) as path:
                font_manager.fontManager.addfont(str(path))
    _fonts_added = True


def rc(variant: Variant, context: Context = "paper") -> dict:
    if context not in _SCALE:
        raise ValueError(f"context must be one of {CONTEXTS}, not {context!r}")
    if variant not in VARIANTS:
        raise ValueError(f"variant must be one of {VARIANTS}, not {variant!r}")
    size, small, lw, ms, frame, major, minor = _SCALE[context]
    common = {
        "font.size": size,
        "axes.titlesize": size,
        "axes.labelsize": size,
        "xtick.labelsize": small,
        "ytick.labelsize": small,
        "legend.fontsize": small,
        "legend.frameon": False,
        "lines.linewidth": lw,
        "lines.markersize": ms,
        "errorbar.capsize": ms * 0.5,
        "axes.linewidth": frame,
        "xtick.major.width": frame,
        "ytick.major.width": frame,
        "xtick.minor.width": frame * 0.75,
        "ytick.minor.width": frame * 0.75,
        "xtick.major.size": major,
        "ytick.major.size": major,
        "xtick.minor.size": minor,
        "ytick.minor.size": minor,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,
        "axes.prop_cycle": cvdkit.pick(8).cycler(),
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.dpi": 300 if context == "paper" else 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        # Embed TrueType rather than Type 3 fonts, which many journals reject
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
    if variant == "box":
        return common | {
            "font.family": "sans-serif",
            "font.sans-serif": SANS,
            "mathtext.fontset": "stixsans",
            "axes.spines.top": True,
            "axes.spines.right": True,
            "xtick.top": True,
            "ytick.right": True,
            "axes.grid": False,
            "axes.edgecolor": "black",
            "axes.labelcolor": "black",
            "text.color": "black",
            "xtick.color": "black",
            "ytick.color": "black",
        }
    _add_fonts()
    return common | {
        "font.family": "sans-serif",
        "font.sans-serif": [PLEX, *SANS],
        "mathtext.fontset": "stix",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.top": False,
        "ytick.right": False,
        "axes.grid": True,
        "axes.grid.which": "major",
        "grid.color": GRID,
        "grid.linewidth": frame * 0.75,
        "axes.axisbelow": True,
        "axes.edgecolor": INK_SOFT,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK_SOFT,
        "ytick.color": INK_SOFT,
        "axes.titlelocation": "left",
    }
