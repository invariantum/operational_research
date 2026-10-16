# Semester 1 · Week 08 – Networks - Shortest Paths and MST

Networks (graphs with weights on the edges) and two classic questions about them. **Shortest path:** the
cheapest route from one vertex to another, found with Dijkstra's algorithm. **Minimum spanning tree (MST):** the
cheapest set of edges that connects every vertex, found with Prim's or Kruskal's algorithm. This week is pen and
paper: you fill in the label tables by hand, exactly as on the slides. Work through the folders in number order.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Lecture slides (PDF, and last year's annotated copy); two short extra decks: *Negative weight example* and *Dijkstra Algorithm* | The lecture |
| `3 Tutorial` | Tutorial sheet: Q1 (MST), Q2 (shortest paths) | The practical |
| `4 Tutorial Answers` | Worked answers, step by step: Q1 (Prim and Kruskal) and Q2 (Dijkstra); a notebook that runs the three algorithms | **Release after the practical** |
| `5 Source Files` | Editable originals (.pptx, .docx), staff note | Staff only; edit here, then republish the PDF |
| `6 Further Reading` | MIT 6.006 lecture notes on Dijkstra (correctness proof and running time) | Optional reading |

## Before you start

- **Week 06:** graphs as vertices and edges (vertex cover, assignment). This week the edges carry weights.
- **Maths:** sets and pairs ($V$, $E \subseteq V \times V$), sums, $\infty$ as "not reached yet", reading a table
  row by row.
- **Python** is only needed for the optional answers notebook: dictionaries, loops and functions (plain Python,
  nothing to install).

## Work through this week in order

Page numbers are the pages of `1 Lecture/Week 8 - Networks - Shortest Paths and MST.pdf` (page = slide).

| Step | File | What it is for |
| --- | --- | --- |
| 1 | Slides, pages 1–6 | Directed networks $G = (V, E)$ with weights $w$, the adjacency matrix, the shortest path problem; the *Blue Peter* example: 0–3–1–4–5, length 15 |
| 2 | Slides, pages 7–28 | Dijkstra's algorithm step by step: permanent and temporary labels, distance $d_v$ and predecessor $\pi_v$; s–d–b–e–t, length **15** |
| 3 | Slides, pages 29–31 | Why it works (each permanent label is a shortest distance; every sub-path of a shortest path is shortest) and its running time |
| 4 | `1 Lecture/Negative weight example (Dijkstra fails).pdf` | Why the weights must be nonnegative: Dijkstra returns 1–2 (length 1), but 1–3–4–2 has length −1 |
| 5 | Slides, pages 36–55 | Minimum spanning trees; Prim's algorithm on the fibre-optic cable example: total **21** |
| 6 | Slides, pages 56–69 | Kruskal's algorithm on a second network: total **21** |
| 7 | `3 Tutorial/Week 8 - Tutorial - Networks - Shortest Paths and MST.pdf` | Q1: MST with Prim and with Kruskal. Q2a, Q2b: shortest paths with Dijkstra. The first page repeats the three algorithms |
| 8 | `4 Tutorial Answers/Week 8 - Tutorial - Networks - Q1 Answers.pdf`, `… Q2 Answers.pdf` | Check every step of your tables |
| 9 | `4 Tutorial Answers/Q1-Q2 answers in Python.ipynb` | Dijkstra, Prim and Kruskal in plain Python: prints each step for the lecture examples, Q1, Q2 and the negative weight example |
| 10 | *Optional:* `1 Lecture/Dijkstra Algorithm.pdf`, `6 Further Reading/MIT 6.006 Lecture 16 - Dijkstra.pdf` | Another walk-through of Dijkstra (with the Bellman-Ford algorithm for negative weights), and the proofs |

Pages 32–35 are a short break (*Where's Wally?*).

The notebook starts with the problem, how to run it and the expected results, explains every code cell, and ends
with a *What do you notice?* and a *Try it* question with hidden answers.

## By the end of this week you can

- describe a network by its vertices, edges and weights, and as an adjacency matrix;
- run Dijkstra's algorithm by hand, keeping the table of labels $d_v$, $\pi_v$, and read off a shortest path by
  working backwards from the destination along the predecessors;
- explain why Dijkstra needs nonnegative weights (and name Bellman-Ford for the other case);
- find a minimum spanning tree with Prim's algorithm (grow one tree from any vertex) and with Kruskal's algorithm
  (add the lightest edge that does not close a cycle), and check that both give the same total weight.

**Next:** Week 09 (Travelling Salesman Problem): the cheapest *tour* through every vertex of a network, solved as
an integer program in Pyomo.

## Tutorial answers

| Question | Answer | Where |
| --- | --- | --- |
| Q1 Prim (from A) | Edges AD 5, DF 6, AB 7, BE 7, EC 5, EG 9: total **39** | Q1 Answers PDF, pages 1–9; notebook |
| Q1 Kruskal | The same tree, total **39** | Q1 Answers PDF, pages 10–20; notebook |
| Q2a (1 → 4) | 1–3–4, length **5**. 1–2–3–4 also has length 5: both are right | Q2 Answers PDF, pages 1–7; notebook |
| Q2b (1 → 2) | 1–3–4–2, length **55** | Q2 Answers PDF, pages 8–14; notebook |

**More than one right answer.** When two labels tie, either vertex or edge may be chosen first. Your tables may
then differ from the answers in the order of the steps, but the shortest distances and the total weight of the
MST are the same.

## Notes for staff

- Files were renamed from *Semester 2 - Week 3* (last year's slot) to *Week 8*; `Djikstras Algorithm.pptx` became
  `Dijkstra Algorithm.pptx` and `negative_weight_example_fail.pptx` became `Negative weight example (Dijkstra fails).pptx`.
- `Week 8 - Networks - Shortest Paths and MST (annotated).pdf` is last year's (2020-21) deck with handwritten
  notes; its text differs slightly from this year's slides.
- `Dijkstra Algorithm` is Brian C. Dean's *Lecture 20. Shortest Paths* (CpSc 212, Clemson University, 2012).
- The two extra decks (Dijkstra, negative weights) had no PDF; PDFs were exported from the .pptx with
  LibreOffice. That export draws the $d$ and $\pi$ table headings of the negative weight deck as tiny pictures
  and lets the last bullet of *Dijkstra Algorithm* page 27 overlap the footer. **Re-export both from PowerPoint.**
- The handbook lists *Transportation and Transhipment* for this week. Worked examples are in Semester 2 Week 01
  (`6 Production-distribution (minimum-cost flow).ipynb`) and Week 10 (`F.B. Knight - transhipment`).
- Staff note from last year: *Do flow shop scheduling problem live* (an empty file whose name is the note).
- The last slide of `Negative weight example (Dijkstra fails)` gave node 4 the label −3 in its table; the graph on
  the same slide and the path 1-3-4 (3 + (−5)) give −2. Corrected to −2 in the `.pptx` and the PDF re-exported
  (12 Oct 2026). Nothing else changed.
- **Lecture slides (Oct 2026).** The `.pptx` in `5 Source Files` was corrected; **the PDF in `1 Lecture` has not
  been re-exported yet** (slide = PDF page): 24–27 "work backwards from the destination t along the predecessors"
  (it said "from the source"); 31 the running times are $O(|V|^2)$ with a simple array and $O((|E|+|V|)\log|V|)$
  with an adjacency list and a binary heap (it said $O(|V|^2\log|V|)$ with an adjacency list), "worst-case", and the
  unfinished "Or check out" now points to the MIT notes in `6 Further Reading`; 56–68 the label on edge B–E said
  10 while the table, and the order in which Kruskal processes the edges, use 4: the label is now 4 (the MST is 21
  either way); 56 Kruskal step 2 selects the lowest-weight *edge* (it said "vertex"); 59 the table heading is
  $w_e$ (it said $d_v$); 36 MST definition ("a connected, weighted, undirected graph … minimum total edge
  weight"); 37 "wishes", "whilst connecting", "minimum cost of connecting"; 7 Dijkstra designed the algorithm in
  1956 (published 1959) to demonstrate the new ARMAC computer (it said "to test the limitations of computing
  power"), "Edge weights", and route planners (not specifically Google) use contraction hierarchies; 5 "is
  minimised" (this year's `.pptx` already had "its" where the PDF says "it's"); 3 "What is w(1,2)?" and "otherwise
  the edge weight would not be well defined"; 32 "Wally"; 34 "Please be patient, there is some high-tech stuff";
  40 "(here D; any start vertex gives the same total weight)", because slide 39 shows the existing cable at A; 70
  the Taha reference. The text on slides 3, 7, 24–27, 31, 40 and 59 sits in boxes with equations that keep a stored
  picture of the old text, which only LibreOffice and old viewers show. **Re-export from PowerPoint.** The small
  Kruskal picture on slide 36 (an image) still shows B–E = 10.
- **Negative weight example (Oct 2026).** Its title said "Question 2a", but the network is not tutorial Q2a; it is
  now "Dijkstra with a negative edge weight". **Re-export the PDF from PowerPoint.**
- **Dijkstra Algorithm (Oct 2026).** Slide 12 "operations" (it said "opeartions"), slide 23 "PageRank".
  **Re-export the PDF from PowerPoint.**
- **Tutorial sheet (Oct 2026), `.docx`.** Q2a and Q2b say "from node 1" (they said "for node 1"); Kruskal step 2
  reads "Select the lowest-weight edge not yet considered; if it does not form a cycle, label it as selected".
  **The Kruskal picture on page 1 is an image that shows B–E = 10 while its table says 4; replace it with the
  corrected lecture slide 57 graph.** The PDF has not been re-exported yet.
- **Q1 answers (Oct 2026), `.pptx`.** The Kruskal tables (slides 11–20) are headed $w_e$ and the total is
  $\sum_e w_e = 39$ (they used $d_v$, the Prim notation). **The PDF has not been re-exported yet.**
- **Q2 answers (Oct 2026), `.pptx`.** Slide 7 adds that 1–2–3–4 also has length 5; slide 2's table heading is
  $i$, like the other slides (it said $v$); slide 10, an unlabelled copy of the Q2b start that was not in the PDF,
  is now hidden. **The PDF has not been re-exported yet.**
- **New (Oct 2026):** `4 Tutorial Answers/Q1-Q2 answers in Python.ipynb` runs Dijkstra, Prim and Kruskal in plain
  Python on the lecture examples, Q1, Q2a, Q2b and the negative weight example; its steps follow the slides and
  answer sheets (15, 21, 21, 39, 5, 55). It has no `.py` source.
