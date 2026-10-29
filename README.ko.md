# qoraplot

[English](README.md) | [한국어](README.ko.md)

matplotlib용 Origin 스타일 출판용 그림 스타일입니다. 네 면 모두 안쪽을 향한 눈금과 보조 눈금, 닫힌 테두리, 격자
없음, 산세리프 글꼴을 쓰고, 저널 단 폭·슬라이드·포스터 크기에 맞춥니다. 색·마커·점선 순환은
[cvdkit](https://github.com/NaNIsaac/cvdkit)에서 가져오므로 색각 이상이 있어도 계열이 구별됩니다.

qoraplot은 OriginLab과 관계가 없으며, "Origin 스타일"은 모양을 설명하는 말일 뿐입니다.

### 스타일 미리보기

| `box` — 논문용 프레임 | `house` — 간결한 레이아웃 |
|---|---|
| ![Origin 스타일 box](docs/variant_box.png) | ![House 스타일](docs/variant_house.png) |

두 스타일 모두 색·마커·점선 순환에 [cvdkit](https://github.com/NaNIsaac/cvdkit)을 사용합니다. [녹색각 이상 시뮬레이션 비교](docs/variants_deutan.png)도 확인할 수 있습니다.

## 설치

Python 3.12 이상이 필요합니다. PyPI에 첫 릴리스가 올라가기 전까지는 이 저장소를 clone한 폴더에서
설치합니다.

<!-- test unix -->
```sh
uv venv
uv pip install .
```

<!-- test windows -->
```powershell
uv venv
uv pip install .
```

import되는지 확인합니다.

<!-- test unix -->
```sh
uv run --no-project python -c "import qoraplot; print(qoraplot.VARIANTS)"
```

<!-- test windows -->
```powershell
uv run --no-project python -c "import qoraplot; print(qoraplot.VARIANTS)"
```

## 사용법

```python
import matplotlib.pyplot as plt
import numpy as np
import qoraplot

qoraplot.use("box", "paper")  # 변형 "box" 또는 "house"; 맥락 "paper", "slide", "poster"

fig, ax = qoraplot.figure("single")  # 폭 3.5 in; "double"은 7.2 in
x = np.linspace(0, 10, 30)
for tau in (1, 2, 4):
    ax.plot(x, np.exp(-x / tau), label=f"tau = {tau}")
ax.set_xlabel("time (ns)")
ax.legend()
qoraplot.panel_label(ax, "a")
fig.savefig("figure.pdf")  # paper는 300 dpi, TrueType 글꼴 포함

with qoraplot.style("house", "poster"):  # 블록 안에서만 적용; 저장도 블록 안에서
    fig, ax = qoraplot.figure(14.4, aspect=0.5)
    ax.plot(x, np.sin(x))
    fig.savefig("poster_panel.png")
```

글꼴은 그림을 그릴 때 정해지므로 `style(...)`을 쓸 때는 `savefig`도 블록 안에서 호출합니다.

## 변형

같은 데이터로 그린 두 변형입니다. 아직 기본값이 없으므로 하나를 고르기 전까지는 호출마다 변형을 지정합니다.

- `box`: 닫힌 테두리, 네 면 안쪽 눈금, 보조 눈금, 격자 없음, Arial 또는 Helvetica(없으면 Liberation Sans,
  그다음 DejaVu Sans), 검은 선.
- `house`: 열린 L자 테두리, 회색 축과 눈금, 거의 검은 글자, 옅은 격자, IBM Plex Sans(포함됨)와 STIX 수식,
  안쪽 눈금.

`box`:

![box variant](docs/variant_box.png)

`house`:

![house variant](docs/variant_house.png)

녹색맹으로 본 두 변형(cvdkit 시뮬레이션): [docs/variants_deutan.png](docs/variants_deutan.png).
그림은 `examples/variants.py`로 그립니다.

## 라이선스

MIT. IBM Plex Sans는 SIL Open Font License 1.1로 포함되어 있습니다
([src/qoraplot/fonts/OFL.txt](src/qoraplot/fonts/OFL.txt)).
