"""Draw the two style variants on the same data, for choosing the default.

Writes docs/variant_box.png, docs/variant_house.png and docs/variants_deutan.png (both variants as
seen with deuteranopia). Run: uv run python examples/variants.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import cvdkit
import matplotlib.pyplot as plt
import numpy as np

import qoraplot

DOCS = Path(__file__).resolve().parents[1] / "docs"


def data():
    rng = np.random.default_rng(7)
    t = np.linspace(0, 10, 40)
    curves = {tau: np.exp(-t / tau) for tau in (1.0, 2.0, 4.0, 8.0)}
    x = np.linspace(0.5, 9.5, 12)
    err = 0.04 + 0.02 * rng.random(x.size)
    y = 0.8 * np.exp(-x / 3.0) + 0.1 + rng.normal(0, err)
    return t, curves, x, y, err


def draw(variant: str) -> np.ndarray:
    """Save the figure for `variant` and return its deuteranopia simulation."""
    t, curves, x, y, err = data()
    # Fonts are looked up when the figure is drawn, so saving stays inside the style block
    with qoraplot.style(variant, "paper"):
        fig, (a, b) = qoraplot.figure("double", aspect=0.36, ncols=2)
        for tau, c in curves.items():
            a.plot(t[::3], c[::3], label=rf"$\tau$ = {tau:g} ns")
        a.set_xlabel("time $t$ (ns)")
        a.set_ylabel("normalised intensity")
        a.legend()
        qoraplot.panel_label(a, "a")

        b.errorbar(x, y, yerr=err, fmt="o", color="black", ms=3.5, label="measured")
        xf = np.linspace(0, 10, 200)
        b.plot(xf, 0.8 * np.exp(-xf / 3.0) + 0.1, marker="", label="fit, $\\tau$ = 3 ns")
        b.set_xlabel("delay (ns)")
        b.set_ylabel("signal (arb. units)")
        b.legend()
        qoraplot.panel_label(b, "b")
        fig.savefig(DOCS / f"variant_{variant}.png", dpi=200)
        return cvdkit.simulate(fig, "deutan")


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    sims = [draw(variant) for variant in qoraplot.VARIANTS]
    width = max(s.shape[1] for s in sims)
    padded = [np.pad(s, ((0, 8), (0, width - s.shape[1]), (0, 0)), constant_values=1) for s in sims]
    plt.imsave(DOCS / "variants_deutan.png", (np.vstack(padded) * 255).round().astype(np.uint8))


if __name__ == "__main__":
    main()
