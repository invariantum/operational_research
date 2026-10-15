# Semester 2 · Week 06 – Agent Based Modelling

Agent-based modelling with the Mesa library: Game of Life, Schelling segregation, Boltzmann wealth, traffic jams and an SIR epidemic.

**Open first:** `1 Lecture/Agent Based Modelling with Mesa - Slides.html`, then the notebooks in `2 Lecture Demos` as each model comes up.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (a single HTML file) | The lecture |
| `2 Lecture Demos` | One notebook per model on the slides | During or after the lecture |

## 1 Lecture

- `Agent Based Modelling with Mesa - Slides.html`. On the site, double-click it: it shows as one long page, because the
  viewer blocks the slide controls until you press *Trust HTML*. For slide mode, press *Trust HTML*, or download the file and
  open it in your browser. The slides also link to online demos (py.cafe Mesa examples, a Colab traffic notebook,
  playgameoflife.com); those need the internet.

## 2 Lecture Demos (added for this site)

Each notebook follows the rules on the slides, asks you to predict before you run, and installs Mesa in its first cell
(`%pip install mesa networkx`; it takes about half a minute the first time). Tested with Mesa 3.5.1 in the browser.

| Notebook | Slides | What to look for |
| --- | --- | --- |
| `1 Game of Life.ipynb` | 8 | Simple local rules → still lifes, oscillators, gliders |
| `2 Schelling segregation.ipynb` | 11–14 | A mild preference (h = 0.3) still gives strong clustering; final similarity vs h |
| `3 Boltzmann wealth.ipynb` | 15–19 | Random exchange → unequal wealth; the Gini coefficient settles near 0.6 |
| `4 Traffic (Nagel-Schreckenberg).ipynb` | 20–23 | Jams with no cause that move backwards; the flow–density curve |
| `5 SIR epidemic.ipynb` | 24–27 | The rise and fall of infections; a small change in β gives a large change in the outcome |

The interactive Solara apps from the slides (py.cafe) do not run on this site. To run Mesa with Solara on your own
computer: `pip install mesa solara`, then copy an example from the py.cafe link.

## Errata and notes

| Where | Note |
| --- | --- |
| Slide 26 (SIR demo) | The original slide image `images/sir.png` was missing from the course files. The slide now shows a chart from one run of `2 Lecture Demos/5 SIR epidemic.ipynb` (seed 1), labelled as illustrative. It is not the original author's image |
| Slide 19 (Gini) | G = 2Σ i·wᵢ / (nΣ wᵢ) − (n+1)/n needs the wealths sorted from smallest to largest (i = 1…n). Its largest value is (n−1)/n, which is close to 1 for large n. The Boltzmann notebook uses this form |
