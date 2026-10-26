from pathlib import Path

import cvdkit
import matplotlib as mpl
import numpy as np
import pytest
from matplotlib import font_manager
from matplotlib import image as plt_image

import qoraplot

BASELINE = Path(__file__).with_name("baseline")


@pytest.mark.parametrize("context", qoraplot.CONTEXTS)
@pytest.mark.parametrize("variant", qoraplot.VARIANTS)
def test_every_key_is_a_valid_rcparam(context, variant):
    params = qoraplot.rc(context, variant)
    assert set(params) <= set(mpl.rcParams)
    with qoraplot.style(context, variant):
        for key, value in params.items():
            if key != "axes.prop_cycle":
                assert mpl.rcParams[key] == mpl.rcParams.validate[key](value), key


def test_box_is_closed_with_ticks_inside_on_four_sides():
    p = qoraplot.rc("paper", "box")
    assert p["axes.spines.top"] and p["axes.spines.right"]
    assert p["xtick.top"] and p["ytick.right"]
    assert p["xtick.direction"] == p["ytick.direction"] == "in"
    assert p["xtick.minor.visible"] and p["ytick.minor.visible"]
    assert not p["axes.grid"]
    assert p["font.sans-serif"][0] == "Arial"


def test_house_is_an_open_frame_in_plex():
    p = qoraplot.rc("paper", "house")
    assert not p["axes.spines.top"] and not p["axes.spines.right"]
    assert p["axes.grid"]
    assert p["font.sans-serif"][0] == "IBM Plex Sans"
    found = font_manager.findfont(font_manager.FontProperties(family="IBM Plex Sans"))
    assert Path(found).name == "IBMPlexSans-Regular.ttf"


def test_sizes_grow_from_paper_to_poster():
    paper, slide, poster = (qoraplot.rc(c)["font.size"] for c in ("paper", "slide", "poster"))
    assert paper < slide < poster


def test_cycle_is_cvd_safe_with_markers_and_dashes():
    cycle = list(qoraplot.rc()["axes.prop_cycle"])
    assert [c["color"] for c in cycle] == list(cvdkit.pick(8).colors)
    assert len({(c["marker"], str(c["linestyle"])) for c in cycle}) == len(cycle)


def test_style_restores_rcparams():
    before = dict(mpl.rcParams)
    with qoraplot.style("poster", "house"):
        assert mpl.rcParams["font.size"] == 26
    assert dict(mpl.rcParams) == before


def test_use_and_bad_arguments():
    with mpl.rc_context():
        qoraplot.use("slide", "box")
        assert mpl.rcParams["font.size"] == 16
    with pytest.raises(ValueError):
        qoraplot.rc("talk")
    with pytest.raises(ValueError):
        qoraplot.rc("paper", "plain")


def test_figure_sizes():
    with qoraplot.style():
        fig, _ = qoraplot.figure("single", aspect=0.5)
        assert tuple(fig.get_size_inches()) == pytest.approx((3.5, 1.75))
        fig, axes = qoraplot.figure(5.0, ncols=2)
        assert tuple(fig.get_size_inches()) == pytest.approx((5.0, 3.75))
        assert len(axes) == 2


def _render(variant: str) -> np.ndarray:
    # Tick labels and text off, so the render does not depend on installed fonts
    with qoraplot.style("paper", variant):
        fig, ax = qoraplot.figure("single", dpi=100)
        x = np.linspace(0, 1, 6)
        for k in range(3):
            ax.plot(x, x * (k + 1) / 3)
        ax.tick_params(labelbottom=False, labelleft=False)
        return cvdkit.simulate(fig, "deutan")


@pytest.mark.parametrize("variant", qoraplot.VARIANTS)
def test_saved_figure_matches_baseline(variant):
    got = _render(variant)
    want = plt_image.imread(BASELINE / f"lines_{variant}.png")[..., :3]
    assert got.shape == want.shape
    # Agg antialiasing can move single edge pixels between matplotlib builds
    assert np.abs(got - want).mean() < 2e-3
