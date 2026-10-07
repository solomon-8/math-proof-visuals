# Lean formalization boundary audit

Repository: `upstream`, read-only audit at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
Audit date: 2026-10-07 UTC. No Lean, Lake, Comparator, package installation, cache fetch, or repository modification was performed.

## Priority conclusion: family 017, irrationality exponent of π

**Limited result:** the manuscript's main theorem, independently specified Comparator target, and solution's top-level theorem state the same substantive claim: μ(π)=2. I found no replacement of the conjecture by an assumption in that top-level result and no obvious gap in the final bridge from the eventual approximation bound to the supremum definition. This is source-level inspection, not a successful kernel/Comparator verification and not a complete mathematical review of the interpolation argument.

Suggested educational narration:

> 这篇仓库论文声称证明 π 的无理性指数等于 2，并提供了以这个完整命题为目标的 Lean 证明源码和 Comparator 检查配置。我们核对了论文与形式化命题的对应关系，但没有在这里独立运行并验证整套形式化证明。

Do not say that this audit established the proof, community acceptance, or a successful Comparator run.

### What the target actually says

For every real ν>2, there exists an integer Q≥2 such that for every integer numerator p and every integer denominator q≥Q,

`q^(−ν) ≤ |π − p/q|`.

In addition, the supremum of positive exponents ν for which there are infinitely many rational r with reduced denominator at least 2 and `0 < |π−r| < r.den^(−ν)` equals 2.

- Manuscript source: `preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/main.tex:50–78`
- PDF: same directory's `paper.pdf`, page 1, Theorem 1.1; its first page was rendered and visually checked
- Independent challenge statement: `lean/ComparatorChallenges/PiExponent.lean:7–15`
- Solution top-level theorem: `lean/OAI/NumberTheory/PiExponent/Main.lean:17–27`
- Formal definitions: `lean/OAI/NumberTheory/PiExponent/Statement.lean:7–23`
- Human-readable declared scope: `lean/docs/017.md:9–11`

The challenge spells out `Real.pi`, the absolute approximation error, and the rational denominator directly using Mathlib; it does not rely on a privately redefined `irrationalityExponent`. Its conjunction is textually the same statement as the solution's `main` (before the proof bodies).

Q is allowed to depend on ν. The paper explicitly says its argument does not produce Q effectively. This result does not assert `|π−p/q| ≥ 1/q²` for all or all sufficiently large denominators, nor a uniform positive bound `c/q²`. In fact, the lower-exponent bridge uses the standard fact that an irrational number has infinitely many rational approximations with error strictly below `1/q²`.

### The last logical bridge is present

`lean/OAI/NumberTheory/PiExponent/Approximation/Exponent.lean`:

- Lines 7–26 convert natural-number and integer-denominator formulations, using Q≥2 to control positivity
- Lines 28–55 prove that only finitely many rationals in a bounded real interval have bounded denominator
- Lines 57–75 use Mathlib's `Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational` to show exponent 2 is in the approximation-exponent set; denominators 1 and zero error are handled
- Lines 77–90 use the eventual lower bound to make good approximations finite for every ν>2
- Lines 92–102 prove both supremum inequalities, providing nonemptiness and upper boundedness for the conditionally complete real supremum
- Lines 104–106 instantiate the result with Mathlib's `irrational_pi`

Thus the use of real-valued `sSup` is not silently relying on the default value of an unbounded/empty supremum in this final argument.

### The deep interpolation claim is not merely an undischarged parameter

`Main.lean:8–9` supplies `AdmissibleMatrixInterpolation.globalInterpolation` to the conditional implication. The supplied theorem is declared without a mathematical assumption at `Approximation/AdmissibleMatrixGeometry.lean:41–44`. It is assembled using eventual jet-surjectivity at `Jets/AdmissibleJetSurjectivity.lean:15–25`.

`Approximation/InterpolationConsequence.lean:9–13` combines it with `LiteralAnalytic.analyticAggregate`, which is declared and given a proof at `Analysis/AnalyticAggregate.lean:96–101`.

`Approximation/DeterminantContradiction.lean:94–106` defines these interpolation and analytic statements concretely in terms of the actual interpolation matrix and determinant. Lines 167–180 construct admissible parameters from the negation of the desired eventual bound, then use the conflicting determinant bounds. The existence step is not omitted: `Approximation/AdmissibleParameters.lean:105` onward gives `exists_admissible_parameters`, with the bad-approximation hypothesis.

This discharges the visible interface assumptions. It does not independently establish every claim in the 869-file local dependency closure or the underlying algebraic-geometry proof.

### Comparator configuration and limitations

`lean/ComparatorChallenges/PiExponent.json:2–13` selects:

- Challenge: `ComparatorChallenges.PiExponent`
- Solution: `OAI.NumberTheory.PiExponent.Main`
- The sole selected theorem: `OAI.PiExponent.main`
- No definition holes (`definition_names: []`)
- Permitted axioms exactly `propext`, `Quot.sound`, `Classical.choice`
- `enable_nanoda: false`

The `sorry` at challenge line 15 is a specification placeholder, not the submitted solution proof. [Comparator's official README](https://github.com/leanprover/comparator) explicitly describes this workflow: a successful properly configured run checks statement agreement, allowed axioms and Lean-kernel acceptance. Its optional extra-kernel check is separate. No such run was performed here; `enable_nanoda: false` by itself does not disable Lean's kernel checks.

A local source import traversal starting at the solution found 869 local OAI modules. External imports are Mathlib modules and Lean's Omega tactic module. A textual scan found no `axiom`, `sorry`, or `admit` marker in this closure. This is weak supporting source evidence, not an axiom-dependency or elaboration certificate. The complete dependency list is in `import_scan.json`.

`PiExponent` and its manuscript are absent from the narrower `formalization.yaml` at this commit, although their dedicated docs, challenge and solution files are present. Do not use that catalogue as evidence that this particular result has been independently checked.

### Flint–Hills scope nuance

The manuscript also states the classical Flint–Hills series converges (`build/main.tex:90–92`, PDF page 1). `lean/docs/017.md:11` says this consequence is outside the selected statement, correctly: the Comparator config selects only `OAI.PiExponent.main`. Nevertheless the solution contains a separate `flint_hills_summable` theorem at `Main.lean:29–32`. Therefore do not say “the repository has no formalized Flint–Hills consequence”; say “it is not included in this Comparator target.”

### Local verification prerequisites checked

The requested toolchain is `leanprover/lean4:v4.34.1`. None of `lean`, `lake`, `elan`, `comparator`, `lean4export`, or `landrun` is on PATH. The repository has no `lean/.lake` directory. The usual `<user-home>/.elan`, `<superuser-home>/.elan`, `/opt/lean`, and `/usr/local/bin/lean` locations are absent. These observations establish no usable local toolchain/dependency setup via the checked paths; they are not an exhaustive disk search. Exact results are recorded in `pi_verification_state.json`.

The minimal selected verification target, after a trusted isolated setup has been provisioned, is `ComparatorChallenges/PiExponent.json` (the repository README uses `lake env comparator <config>`). This was not invoked. `lean/lakefile.lean:262–275` performs dependency preparation during configuration elaboration, including clone/checkout at lines 243–254, so even a seemingly read-only `lake env` could mutate/download dependency trees. No automatic installation or download was attempted.

## Repository-wide inventory boundaries

Counts are source inventory, not counts of successfully checked proofs:

- 722 manuscript directories under `preprints/`, matching the top-level README
- `formalization.yaml`: 162 paper-source records, 185 main-result records, 30 related-formalization records
- 178 unique Comparator configs are referenced by those 185 records (some configs check multiple declarations)
- 405 Comparator JSON files exist, containing 507 theorem-name entries and 506 distinct theorem names
- All 405 configs permit precisely the same three standard axioms, with two ordering variants
- Nanoda setting: 402 explicitly false, 1 explicitly true (`ArtinParabolicIntersections.json`), 2 omitted (`UniversalTensorSquares.json`, `KadisonRingrose.json`)
- All 162 manifest paper paths and all main-result file/config paths exist
- `formalization.yaml:914–917` declares its scope “Partial progress.”
- `formalization.yaml:1662–1663` declares review status “unchecked”

This metadata should not be turned into a mathematical error allegation or a claim that any particular theorem has failed verification.

## Other sampled targets (brief, deprioritized)

### Symmetric Mahler inequality

`ComparatorChallenges/MahlerConjecture.lean:15–20` and `OAI/Analysis/Mahler/MainTheorem.lean:12–22` state the usual inequality for every positive dimension and compact convex origin-symmetric set with nonempty interior, using ordinary Lebesgue volume and a directly defined coordinate polar. The source theorem has no extra conjectural premise. There are 229 local files in the traversed import closure and no textual `axiom/sorry/admit` hits. Scope docs separately discuss equality and general nonsymmetric results; these do not belong to this particular target. This was a statement-level check, not a complete comparison with the PDF or a verified build.

### Characteristic-two Kaplansky direct-finiteness counterexample

`ComparatorChallenges/KaplanskyDirectFiniteness.lean:7–13` fixes `MainClaim` as existence of a finite field of characteristic 2 and a finitely generated group whose group algebra has a one-sided inverse that is not two-sided. `OAI/RingTheory/DirectFiniteness/Main.lean:9` supplies the theorem via `Prescription.Output.prescribed_main`. This target does not require the group to be torsion-free. Scope docs `lean/docs/197.md` explicitly distinguish the characteristic-two, detailed finitely presented, determinant, and odd-characteristic statements. There are 121 local files in the traversed import closure; the sole raw `admit` text match is the English verb in a doc comment, not a proof hole. No mathematical-error claim follows from this sample. The PDF comparison was deferred when family 017 was prioritized.

## Evidence files

- `inventory.json`: source counts, missing-path checks, duplicate manifest config references
- `import_scan.json`: exact local import closure and raw textual marker hits for the three sampled solution modules
- `pi-paper.txt`: `pdftotext -layout` extraction for navigation, not a substitute for source/rendered equations
- `pi-paper-page-1.png`: rendered theorem page, visually checked
- `audit_inventory.py`: reproducible static inventory and import scan
- `pi_verification_state.json`: literal target-equality check, tool locations, known dependency directories, source hashes
- `audit-output.txt`: recorded successful static script output

The repository remained unchanged. The critical unperformed check is actual elaboration and Comparator verification in a suitably isolated, trusted environment with the pinned dependencies.
