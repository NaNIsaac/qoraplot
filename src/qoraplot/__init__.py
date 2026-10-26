"""Origin-like publication style for matplotlib, with colour-vision-deficiency-safe cycles."""

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .styles import CONTEXTS, VARIANTS, Context, Variant, rc

# About 89 mm and 183 mm, the usual single- and double-column widths of journals
WIDTHS = {"single": 3.5, "double": 7.2}

__all__ = ["CONTEXTS", "VARIANTS", "WIDTHS", "figure", "panel_label", "rc", "style", "use"]


def use(context: Context = "paper", variant: Variant = "box") -> None:
    """Apply the style to every later figure."""
    mpl.rcParams.update(rc(context, variant))


@contextmanager
def style(context: Context = "paper", variant: Variant = "box") -> Iterator[None]:
    """Apply the style inside a `with` block only."""
    with mpl.rc_context(rc(context, variant)):
        yield


def figure(
    width: str | float = "single", aspect: float = 0.75, nrows: int = 1, ncols: int = 1, **kwargs
) -> tuple[Figure, Any]:
    """`plt.subplots` sized for a journal column: `width` is "single", "double" or inches, and
    the height is `aspect` times the width."""
    w = WIDTHS[width] if isinstance(width, str) else float(width)
    kwargs.setdefault("layout", "constrained")
    return plt.subplots(nrows, ncols, figsize=(w, w * aspect), **kwargs)


def panel_label(ax: Axes, label: str, **kwargs) -> None:
    """A bold panel letter just outside the top-left corner of `ax`."""
    kwargs = {"fontweight": "bold", "va": "bottom", "ha": "right"} | kwargs
    ax.text(-0.02, 1.02, label, transform=ax.transAxes, **kwargs)
