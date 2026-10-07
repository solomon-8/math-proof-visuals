# 首批三集：条件、归属与引用

Snapshot: OpenAI `math`, commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, reviewed 2026-10-07 UTC.

These are editorial explainers of repository claims. The manuscript text, Lean statement, solution-module presence, and third-party acceptance are separate evidence layers. A selected challenge containing `sorry` is a specification; its solution and comparator configuration must be checked instead. No independent Lean compilation or mathematical certification is claimed here.

## 017 — π 的有理逼近 / Rational approximation to π

Author: OpenAI. Date: 24 September 2026. Title: The irrationality exponent of π is 2.

- [Pinned paper](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/paper.pdf)
- [Paper README and requested BibTeX](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/README.md)
- [Scope](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/017.md)
- [Comparator](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/PiExponent.json)

Exact claim: for every real ν>2, an integer Q(ν) exists so that every integer p and every integer q≥Q(ν) satisfy |π−p/q|≥q^(−ν). This is an eventual statement, including unreduced fractions. Q depends on ν and the proof does not make it effective. It does not assert a uniform positive c/q² bound or bounded continued-fraction partial quotients. It does not supply a faster π-digits algorithm.

The Flint–Hills series consequence is in the manuscript; it is outside the selected PiExponent comparator statement. An auxiliary Lean source theorem exists, but that alone is not a verified build result.

Primary historical anchors: [Zeilberger–Zudilin, 2019/2020](https://arxiv.org/abs/1912.06345), upper bound 7.103205334137…; [Bai, September 2026 preprint](https://arxiv.org/abs/2609.11276), claimed bound <7.101862832357. Do not label the 2019 number the latest 2026 record.

Suggested attribution: “Based on OpenAI, ‘The irrationality exponent of π is 2’ (2026), openai/math, commit adc7f124… . This video explains the claim; it is not an independent verification.”

## 158 — 平面需要几种颜色 / How many colors does the plane need?

Author: OpenAI. Date: 23 September 2026. Title: The Euclidean plane is not five-colorable.

- [Pinned paper](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/paper.pdf)
- [Paper README and requested BibTeX](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/README.md)
- [Scope](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/158.md)

Exact claim: every coloring c:R²→{1,…,5} has a same-color pair exactly one unit apart. Arbitrary color classes are allowed, with no measurability or continuity assumption. Combined with the classical seven-color construction, the claimed range becomes 6≤χ(R²)≤7. Neither χ=6 nor χ=7 is proved. This is a unit-distance graph problem, distinct from planar map adjacency; do not confuse it with the four-color theorem.

The construction for seven colors uses triangular-lattice Voronoi hexagons of circumradius 2/5 and an index-seven sublattice. Boundary points are assigned to incident hexagons; the strict distance gaps make this valid.

Historical primary source: [de Grey, 2018](https://arxiv.org/abs/1804.02385) proves lower bound five via a finite unit-distance graph. This is the established earlier comparison, not evidence certifying the new bound six.

## 107 — 矩阵乘法的指数 / The matrix-multiplication exponent

Author: OpenAI. Principal paper date: 2 October 2026. Title: An Upper Bound of 9/4 for the Matrix Multiplication Exponent.

- [Pinned paper](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026/paper.pdf)
- [Paper README and requested BibTeX](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026/README.md)
- [Scope](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/107.md)

Exact claim: ω(C)≤9/4, hence for every ε>0 square n×n matrix multiplication over C can use Oε(n^(9/4+ε)) arithmetic operations. It does not assert an exact O(n^2.25) bound, bit complexity, numerical stability, GPU throughput, or a practical finite-size speedup. The manuscript explicitly does not claim competitive estimates at practical matrix sizes.

Primary comparison: [Dupont et al., August 2026](https://arxiv.org/abs/2608.16884), ω<2.371177, supersedes the 2.371339 historical comparison. [NVIDIA matrix multiplication background](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html) supports the real-world relevance of matrix products to neural-network layers, not implementation of this new mathematical construction.

## Publication checklist

The repository root and Lean directory carry Apache-2.0. The per-paper READMEs credit OpenAI and provide specific BibTeX blocks. Both metadata/catalogue text and copied original figures/source remain upstream material; our selection, paraphrases, graphics and commentary must be distinguishable.

- Include the original Apache-2.0 license when distributing copied or derivative upstream materials
- Preserve applicable attribution/copyright notices; mark changed copied files prominently
- No upstream NOTICE file was found in the checked snapshot; still preserve any notices present in materials actually reused
- Credit each paper, date and exact snapshot; link original paper and scope rather than imply independent authorship
- Apache-2.0 does not grant endorsement or general trademark/logo rights
- External historical papers have their own licenses. Link and paraphrase them; do not copy their figures automatically
- Original animations should illustrate assumptions and quantifiers. Do not label finite numerical plots as a proof

This is a factual license-source checklist, not a legal opinion. No publication or upload was performed by this research worker.
