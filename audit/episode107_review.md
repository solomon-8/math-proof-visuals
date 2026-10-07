# Episode 107 mathematical scope review

Reviewed source snapshot: `openai/math` commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a` (read-only). This is a bounded source-and-exposition review, not an independent Lean build or verification of every dependency.

## Source findings

- **Main result:** `ω(ℂ) ≤ 9/4 = 2.25`. Equivalently, for each real `ε > 0`, there is a positive constant `Cε` such that every positive integer size `n` admits a correct finite division-free program with at most `Cε n^(9/4+ε)` arithmetic operations. The constant and chosen algorithm may depend on `ε`.
- **Operations:** additions, subtractions, and multiplications each count one; inputs and constants cost zero. Correctness is exact over complex inputs. There is no bit-complexity, floating-point stability, wall-clock, GPU, or practical crossover guarantee.
- **Do not strengthen:** `ω ≤ 2.25` does not assert `ω = 2.25`, `ω < 2.25`, or a uniform `O(n^2.25)` bound without positive slack.
- **Source versions:** `lean/docs/107.md` still lists the September 24 paper *Complex Matrix Multiplication Below 2.258 and Rectangular Bounds* first, but its scope already says `ω(ℂ) ≤ 9/4`. The newer October 2 paper, *An Upper Bound of 9/4 for the Matrix Multiplication Exponent*, states the `Oε(n^(9/4+ε))` theorem directly. The stronger current result implies the older `<2.258` headline.
- **Formal target:** comparator JSON points to `OAI.LinearAlgebra.MatrixMultiplication.Main`, whose square theorem delegates to `AuxiliarySeparation.omega_le_nine_quarters`. `AuxiliarySeparation/Main.lean` also states the full finite-program cost bound directly. Comparator `sorry` placeholders are challenge statements, not the solution proof.
- **Distinct results:** the dual bound `α > 0.465` and rectangular bound `ω(ℂ;1,0.709,1) < 2.092` are separate. Docs107's all-field `<2.371054886006746` result is also separate; do not extend the complex `9/4` claim to every field.

## Tensor example requirements

- Matrix multiplication can be encoded as `Σᵢⱼₖ xᵢⱼ yⱼₖ zₖᵢ`; pairing output coordinates instead with `zᵢₖ` is an equivalent relabeling when used consistently. The third leg records outputs rather than multiplying three input matrices.
- A full direct sum uses disjoint variables on **all three** legs. Shared-leg blocks are not yet independent matrix products.
- If the finite separation construction is pictured, it uses `5M` source copies and yields `M` full direct-sum blocks, each carrying an `M`-dimensional auxiliary dot product. The dot-product index is not an extra full-direct-sum block index.
- A small tensor/Strassen example may illustrate encoding or recursion; it must not be represented as the full construction that proves exponent `2.25`.

## Inspected evidence

`lean/docs/107.md`; `lean/ComparatorChallenges/MatrixMultiplication.lean` and `.json`; `lean/OAI/LinearAlgebra/MatrixMultiplication/Main.lean`, `Model.lean`, `Arithmetic/Complexity.lean`, `Arithmetic/Exponent.lean`, `AuxiliarySeparation/Main.lean`; October 2 preprint README, `build/paper.tex` (definitions, principal theorem, finite separation, and final arithmetic conversion), and PDF pages 1–3 via text extraction. The PDF's stated theorem agrees with its TeX source.

## Bilingual script review

Read `episodes/107/script.json`, `SCRIPT_en.md`, and `SCRIPT_zh.md` (282-second version). The main statement, epsilon quantifiers, exact output-marker tensor encoding, shared-X structure, label-square mechanism, `5M`/`M`/`M` counts, polynomial profile bounds, and arithmetic-versus-practical limitations agree with the inspected sources. No substantive scope error found.

The following three small script edits were requested and are now present:

1. Say **finite division-free** arithmetic program explicitly in both languages.
2. Introduce the positive parameter `t > 0` for each tensor character, with `λ(T_n) = n^(3t)`, before the growth comparison. The final renderer explicitly shows `t=t(λ)>0`.
3. Replace the label “not its missing lemmas” / “未展示的引理仍需证明” with “Intermediate lemmas are not shown in this animation” / “动画未展示中间引理”. The current wording might incorrectly suggest that proofs are missing from the manuscript.

## Renderer and sample review

Read `episodes/107/render.py` and inspected both-language samples of the main claim and growth scene plus English row/column, tensor, shared-leg, label, polynomial, and exponent scenes. Independently recomputed the sample matrix product as `[[4,2,1],[1,3,1],[4,2,3]]`; the implementation agrees. Tensor indices and polynomial output bins are consistent, and the log-log power plots have the correct slopes and are marked as unit-constant illustrations.

Final corrections verified before lock:

- The label grid shows `M=3`. Because it is labeled as occurring **after** the Fourier constraint, `(g,h)=(1,3),(3,1)` must have zero support: `u−v+2(g−h)=0` is impossible for these pairs with `u,v∈{1,2,3}`. The revised code correctly masks both corners throughout. An independently generated early frame (`episodes/107/qa/review_labels_early.png`, local scene time 2 seconds, `δ=1`) visibly confirms their absence. This was a diagram issue, not an error in the paper.
- The growth card now explicitly shows `t=t(λ)>0`.
- Updated screenshots visibly separate the tensor sum's lower indices from the selected monomial, the reciprocal denominators from the comparison caption, and the exponent-curve labels.

**Disposition: mathematical exposition may be locked.** Source consistency, bilingual scope, renderer arithmetic/indexing, and sampled mathematical visuals pass this bounded review. No independent Lean compilation, exhaustive video-frame inspection, or comprehensive proof certification was performed.

Reviewed artifact SHA-256 values:

- `script.json`: `1007dbb579d8a0d2487ca036ab744dbdf902e223f92181f8e9dca72a43a43c9b`
- `render.py`: `f3c7ab78eae9ece5c801e4d5978232038cdb663630d3aa36d345ffdd769b6e35`
