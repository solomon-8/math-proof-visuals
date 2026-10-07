# Algorithm families: editorial ranking and verification scope

Repository inspected read-only at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. This is a source-and-scope audit, not a fresh proof review or a reproduced Lean build. The repository README says results are at different verification stages and some unformalized results could have issues. All claims below are attributed to this repository. No benchmark, external validation of these new repository proofs, or community acceptance was established. The parent separately checked the prior matrix-multiplication baseline against arXiv: https://arxiv.org/abs/2608.16884 (2026-08-17), ω < 2.371177. This supports the historical baseline, not the validity of the new 2.25 proof.

## Recommendation

**Lead with family 107, matrix multiplication.** It combines a large, legible mathematical improvement (the exponent bound 9/4 = 2.25), a familiar computational operation, a formal theorem whose actual endpoint matches the headline, and a caveat that fits in one sentence: it is an asymptotic exact-arithmetic result, with no competitive finite-size or practical GPU claim.

Suggested order within these five, balancing explainability, theoretical consequence, and how well the formalization matches the headline:
1. **107 Matrix multiplication**: strongest broad-audience lead
2. **102 Unique Games**: arguably the deepest complexity-theory story here, but requires more explanation; strong matching formal statement
3. **109 Integer multiplication**: exceptionally accessible historic-barrier hook, but no accompanying formalization found and the explicit saving is astronomically tiny
4. **120 Exact matching**: intuitive pairing problem with a strong near-input-linear claim, but no accompanying formalization found; randomized and asymptotic
5. **130 Fourier transform**: impressive but hardest to communicate safely because the formally represented result is substantially narrower than the all-length headline

The parent's cross-discipline ranking places 107 third for overall communication and first for potential real-world relevance. The order above is only within the five algorithm families. This is an editorial ranking, not an objective ranking of mathematical importance. If the audience is theoretical computer scientists, 102 can reasonably be first. If broad relevance to signal processing matters, 130 can move up only with its verification/model caveats prominent.

## 107: Matrix multiplication

### Exact claim and conditions

The October 2 paper, *An Upper Bound of 9/4 for the Matrix Multiplication Exponent*, Theorem 1.1, asserts:

For every ε > 0, two n × n matrices over the complex numbers can be multiplied in Oε(n^(9/4 + ε)) scalar arithmetic operations. Thus ω(C) ≤ 9/4.

The ε, its dependent constant, and the asymptotic nature matter. Do not replace this with an exact O(n^2.25) claim, equality ω = 2.25, or an optimality claim. The headline bound is over C; it is not the 9/4 bound over every field.

Family companions separately assert:
- square exponent < 2.258 in characteristic zero and outside a finite set of positive characteristics
- dual rectangular exponent α > 0.465 in characteristic zero
- square exponent < 2.371054886006746 over every fixed field

The October 2 square result is the strongest complex headline, and should not be confused with the earlier 2.258 paper.

### Formalization scope

The family documentation explicitly describes finite division-free programs counting additions, subtractions, and multiplications with arbitrary positive exponent slack.

- `lean/OAI/LinearAlgebra/MatrixMultiplication/Main.lean`: `complex_omega_le_nine_quarters : Arithmetic.omega ℂ ≤ (9 : ℝ) / 4`
- `lean/OAI/LinearAlgebra/MatrixMultiplication/AuxiliarySeparation/Main.lean`: `matrix_multiplication_cost_le` states the stronger directly usable quantifiers: for every ε > 0, one C > 0 bounds the cost of a correct program at every n ≥ 1
- `lean/ComparatorChallenges/MatrixMultiplication.lean` independently defines the actual arithmetic programs, correctness for all matrix inputs, and the exponent; the endpoint is not merely an inequality about an undefined surrogate
- Comparator configuration permits only `propext`, `Quot.sound`, and `Classical.choice`

This formal endpoint is a family of finite arithmetic programs. It is not an executable practical implementation, a floating-point error analysis, or a bit-operation/runtime guarantee. I did not run Comparator or Lean. The `sorry` placeholders in Comparator challenge statements are expected challenge targets, not evidence that the solution modules are unfinished. No `sorry` or `axiom` token was found by the limited grep of the AuxiliarySeparation subtree; this is not a whole-dependency audit.

Minor documentation issue: `lean/docs/107.md` lists the earlier companion papers but does explicitly give the stronger 9/4 scope; `formalization.yaml` also includes the October 2 title. Do not infer that the missing October 2 link in that short doc makes the theorem absent.

### What it means / does not mean

At large enough sizes, the claimed number of exact scalar operations grows with an exponent at most 2.25 plus arbitrary slack. The paper itself explicitly says its proof does not specify a competitive finite matrix size. It does not demonstrate a faster GPU kernel, cheaper current AI training, bounded coefficients, stable floating-point evaluation, or a practical crossover point.

The source places its result against a cited previous exponent below 2.371177. The parent independently checked the 2026-08-17 arXiv baseline [arXiv baseline paper](https://arxiv.org/abs/2608.16884). This is the appropriate comparison; do not call 2.371339 the latest baseline. The change in upper-bound exponent is about 0.121177, not a fixed percentage speedup. Safe wording is “the repository claims a substantial reduction in the matrix-multiplication exponent.”

### Explainable mechanism

Matrix multiplication is encoded as a three-way coefficient array, or tensor. The proof develops a method to separate partially overlapping blocks, applies it to polynomial multiplication, and turns bounds on the growth of tensor invariants into the 9/4 exponent. A short explainer can stop at “reorganizing many multiplications together lets the proof save work across the whole computation.” Do not pretend the proof just discovers one small matrix multiplication trick suitable for direct deployment.

### Sources

- [Paper TeX](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026/build/paper.tex): Introduction / Theorem 1.1, and “Route to the exponent”
- [Paper PDF](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026/paper.pdf)
- [Formalization scope](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/107.md)
- [Arithmetic endpoint](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/OAI/LinearAlgebra/MatrixMultiplication/AuxiliarySeparation/Main.lean)
- [Independent statement](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/MatrixMultiplication.lean)

## 102: Unique Games

### Exact claim and conditions

For every fixed ε, δ ∈ (0, 1/2), there is a deterministic polynomial-time reduction from 3SAT to explicitly written, nonempty, unweighted, simple bipartite Unique Games instances over K = F₂^s, s ≥ 1:
- satisfiable formula ⇒ optimum constraint satisfaction fraction at least 1 − ε
- unsatisfiable formula ⇒ optimum fraction at most δ

Every constraint is a translation a(v) = a(u) + c over K. The alphabet size, polynomial degree, and constants depend on ε and δ, which are fixed before the input varies.

Plain example: set ε = δ = 0.01. The theorem says distinguishing instances where some labeling satisfies at least 99% of constraints from ones where no labeling satisfies more than 1% is NP-hard. It concerns finding/distinguishing the best labeling, not checking a supplied labeling.

### Formalization scope

`lean/docs/102.md`, `lean/OAI/Computability/UniqueGames/Theorem.lean`, and `lean/ComparatorChallenges/UniqueGamesTheorem.lean` match these quantifiers. The comparator's `BinaryGapReduction` includes:
- fixed finite alphabet and F₂-vector-space identification
- simple bipartite and translation properties for every output
- a finite-alphabet Turing-machine polynomial-time contract measured on the original binary input
- the completeness and soundness fractions

Main endpoint: `OAI.UniqueGamesTheorem.theorem11`. The configuration allows only the three standard listed axioms. I inspected the source contract, not an executed proof check.

The family also includes separate formal endpoints for optimal Max-Cut hardness, Vertex Cover, Min-UnCut, and directed feedback vertex set. This inspection did not reproduce those proofs.

### Consequences and limits

The paper's consequences section clearly says:
- Max-Cut NP-hardness above the Goemans–Williamson ratio, approximately 0.87856, at every fixed strictly better ratio
- Vertex Cover NP-hardness at every fixed approximation factor strictly below 2
- the reductions/thresholds are earlier authors' results whose Unique Games hypothesis this paper supplies

“Efficient algorithms cannot beat this” requires P ≠ NP for deterministic polynomial-time algorithms. The claimed theorem does not prove P ≠ NP. It also does not say all real-world instances are hard, or that heuristics cannot improve on these bounds on particular data. The direct companion reductions are independent within the family, so the UGC paper should not be credited with inventing every threshold.

### Sources

- [Main theorem TeX](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Unique-Games-Theorem-September-23-2026/build/sections/00-introduction.tex)
- [Consequences and P ≠ NP qualification](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Unique-Games-Theorem-September-23-2026/build/sections/07-consequences.tex)
- [Formalization scope](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/102.md)
- [Independent exact contract](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/UniqueGamesTheorem.lean)

## 109: Integer multiplication below n log n

### Exact claim and conditions

One deterministic Turing machine, with a fixed finite alphabet and a fixed finite number of one-dimensional tapes, multiplies every pair of n-bit nonnegative integers exactly, for every n ≥ 1, in worst-case time

O(n (lg n)^(1 − κ)), with κ = 2^(-182), lg n = max(ceil(log₂ n), 1).

The input is x#y for equal-length binary strings and output is the product padded to 2n bits. This is an ordinary multitape bit-model claim, not just unit-cost complex arithmetic. The source claims it disproves the Schönhage–Strassen n log n optimality conjecture in this model.

### Significance and caution

The historical-barrier story is extremely strong and easy to understand. But κ is about 1.63 × 10^-55. The paper explicitly calls constants and thresholds “extremely large” and says the purpose is a bit-complexity bound. Even a correct theorem gives no reason to expect faster ordinary multiplication at practical sizes.

No family 109 Lean doc exists at this commit; the catalogue does not list this paper as a formalized main result and CONTENTS gives no Lean link. Say “no accompanying formalization located in this release,” not “proved false” or “unverifiable.” Do not transfer Fourier-circuit formalization credit to this stronger finite-tape precision-sensitive theorem.

The paper also asserts exact division and integer square root in the same asymptotic time using classical reductions. Those are subsidiary claims, not a practical calculator speedup.

### Source

- [Actual theorem and explicit impractical-constants warning](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/00-introduction.tex)
- [PDF](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/paper.pdf)

## 120: Almost-linear exact matching

### Exact claim and conditions

Input: any simple undirected unweighted graph G = ([n], E), n ≥ 1, m edges, represented by adjacency lists, including isolated vertices; p = n + m.

One uniform randomized word-RAM algorithm, fixed word-size constant c₀ ≥ 2, fixed C ≥ 1, and a nonincreasing nonnegative η(p) → 0 satisfy:
- every random computation path halts within C p^(1 + η(p)) instructions
- with probability at least 2/3, output is an explicit matching of maximum cardinality

Word length is ceil(c₀ log₂(n+2)); random bits, data movement, multiword arithmetic, initialization, and output are charged.

The same asymptotic and success guarantees extend to deciding and constructing an f-factor for prescribed admissible vertex degrees 0 ≤ f(v) ≤ deg(v).

### Interpretation and limitations

An easy visual story is choosing the greatest possible number of disjoint compatible pairs. The claimed runtime is almost linear in the size of the input, not in n alone for dense graphs: sparse m = O(n) gives n^(1+o(1)); dense m = Θ(n²) gives n^(2+o(1)).

“Exact” describes the optimal matching returned on successful runs. This is not a deterministic or always-correct Las Vegas guarantee: success probability is at least 2/3. It concerns cardinality, not arbitrary maximum-weight matching, stable matching, or counting the number of matchings (the FPRAS family is 113).

The uniformization proof uses dovetailing across fixed-parameter algorithms and does not give a convergence rate for the vanishing exponent. There is no benchmark or practical crossover claim.

No family 120 Lean doc or catalogue entry for the paper was found, and CONTENTS gives no Lean link. Do not confuse the unrelated `LoopMatching` or `MatchingCount` formalizations with this result.

### Sources

- [Theorem, computational model, and uniformization caveats](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Almost-Linear-Time-Maximum-Cardinality-Matching-in-Sparse-General-Graphs-September-24-2026/build/sections/01-introduction.tex)
- [PDF](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Almost-Linear-Time-Maximum-Cardinality-Matching-in-Sparse-General-Graphs-September-24-2026/main.pdf)

## 130: Exact Fourier transforms

### Two different claims must remain separate

**Stronger all-length manuscript:** *An explicit power saving for the exact discrete Fourier transform* asserts one deterministic algorithm computes Fₙx exactly for every positive n and x ∈ Cⁿ. Running time is

O(n (log n)^θ (log log n)^(4 − θ)), where θ ≈ 0.99999999999978935615699598,

and consequently O(n (log n)^(1 − 10^-13)) = o(n log n).

Model conditions are crucial:
- unit-cost exact complex field operations
- unrestricted coefficients and intermediate magnitudes
- one specified root of unity supplied, order D* < 1024 n³
- logarithmic-word address arithmetic/random access charged
- scalar preparation, schedule construction, and array organization charged
- no finite-precision, conditioning, or numerical-stability assertion

The source explicitly says constants are enormous and gives no useful crossover estimate. It expressly rules out inferring stable floating-point FFT speedups, bit-complexity improvements, finite-field results, or formal power-series results.

**Narrower formally represented companion:** *Finite tensor savings and exact Fourier circuits* proves the existence of exact nonuniform complex scalar circuits for an unbounded sequence of lengths with arbitrarily small normalized gate count:

For every c > 0 and cutoff N₀ ≥ 2, there is n ≥ N₀ and a circuit computing Fₙ with fewer than c n log₂ n gates.

Equivalently liminf L(n)/(n log₂ n) = 0. This is not an all-length o(n log n) theorem.

Its scalar additions, subtractions, and predetermined-scalar multiplications each cost one gate. Coefficient generation is outside the model; coefficients may have arbitrary magnitude/description complexity. Permutations and fanout/output references are uncharged. Storage and conditioning are unrestricted.

### Formalization mismatch to avoid

`lean/docs/130.md` expressly states that formalization is subsequential, with no all-length, bounded-coefficient, conditioning, or bit-complexity claim. The actual `MainStatement` in `ComparatorChallenges/ExactFourier.lean` has exactly those “for every c and cutoff, some n” quantifiers. Endpoint `OAI.ExactFourier.main_theorem` matches it, and the solution additionally proves the liminf version.

Thus “the all-length FFT breakthrough is Lean-verified” would misrepresent the visible formalization. “A related exact-circuit result has an accompanying Lean formalization” is accurate. The bounded-coefficient classical lower bounds are not contradicted because the hypotheses differ.

### Sources

- [All-length theorem, arithmetic model, and warnings](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/introduction.tex)
- [Subsequence theorem and nonuniform model](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Finite-tensor-savings-and-exact-Fourier-circuits-September-25-2026/build/sections/01-introduction.tex)
- [Formalization scope](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/130.md)
- [Independent formal statement](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/ExactFourier.lean)

## Safe bilingual hooks for the lead

English: “A new manuscript in OpenAI’s math repository claims the matrix-multiplication exponent is at most 2.25, with a matching Lean formalization. That changes the theoretical growth rate; it does not establish faster AI training on today’s hardware.”

简体中文：“OpenAI 数学仓库中的一篇新论文声称，将矩阵乘法指数的上界推进到 2.25，并附有对应的 Lean 形式化证明。它改变的是理论计算量的增长率，还不能据此说今天的 AI 训练会更快。”

More compact headline pair:
- “A 2.25 exponent for matrix multiplication?”
- “矩阵乘法的指数上界，推进到 2.25？”

Keep “claimed/repository reports” or an equivalent evidence-status sentence visible until independent verification is established. “Matching formalization supplied” is supported by this audit; “I verified the proof in Lean” is not.

## Checks performed / not performed

Performed: verified commit hash; read actual theorem sections, model restrictions, companion distinctions, formalization docs, catalogue entries, source endpoints, and comparator contracts/configurations; confirmed no modifications in source repo using `git status --porcelain`.

Not performed: full mathematical peer review, compilation, Comparator execution, independent external corroboration, practical implementation, numerical benchmark, or full imported-axiom/dependency audit.


## Evidence-status labels for the overall inventory

- 107: manuscript in source catalogue; family scope doc; matching theorem/Comparator source present; compilation not performed by this worker
- 102: manuscript in source catalogue; family scope doc; matching theorem/Comparator source present; compilation not performed by this worker
- 130: the finite-circuit companion is in the source catalogue with a matching scope doc and theorem source; the all-length explicit-power-saving paper is a separate, stronger claim and not the stated formalization target
- 109 and 120: no matching source-catalogue entry or family scope doc located; manuscript-only evidence in this audit

A catalogue entry or scope doc is not a completed proof-verification run. None of these should be added to a count of independently compiled/verified proofs on the basis of this audit.
