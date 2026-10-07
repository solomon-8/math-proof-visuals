# Episode 158: mathematical review

Commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Source/script review on 2026-10-07 UTC. This is a bounded educational-script audit, not a new validation of the manuscript's five-color impossibility theorem. No Lean compilation.

## Source statement and formalization boundary

- `preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/build/sections/introduction.tex`: Theorem1.1 states no proper five-coloring for arbitrary color classes, in ZFC; combined with the elementary seven-color construction, this yields only the alternatives six or seven
- `lean/docs/158.md` states the same scope, including arbitrary starting colorings and all boundary points for the upper bound
- `lean/ComparatorChallenges/EuclideanFiveColor.lean:7–11` defines properness using complex-plane Euclidean norm exactly one, and asserts no `ℂ → Fin 5` proper coloring
- `lean/OAI/Geometry/PlaneColoring/Coloring.lean:7–8` uses the same definition; `Five.lean:124–127` supplies the theorem by applying `proper_to_borel_weak` and then `no_measurable_weak_five_coloring`
- `BorelTransfer.lean:436–443` constructs a Borel weak coloring from an arbitrary proper coloring. It does not require the starting coloring to be measurable. The internal transfer theorem is not fully audited here
- The seven-color Comparator and `Seven.lean:36–37` state the unrestricted proper upper bound. The source formalization uses its own quantitative lattice covering estimates; the animation's `r=2/5` illustration follows the manuscript's elementary construction directly
- Both Comparator configurations permit only `propext`, `Quot.sound`, and `Classical.choice`; no compiler/Comparator execution was performed

The video should keep the five-color result attributed to the manuscript, never infer that six colors work or that seven are necessary, and retain the statement that no independent Lean build or expert acceptance was established.

## Independently checked elementary constructions

Exact script: `check_episode158.py`; output: `evidence/episode158_geometry.json`.

### Seven-color hexagonal tiling

Proposed renderer geometry:

- Circumradius `r=2/5`
- Triangular-lattice basis `(√3r,0)` and `(√3r/2,3r/2)`
- Hexagon vertex angles `30°+60°k`
- Color `(a+3b) mod7`

For a center displacement `(a,b)`, squared distance is `3r²(a²+ab+b²)`. Same color implies `a+3b=7k`, so

`a²+ab+b² = 7(b²−5bk+7k²)`.

For a nonzero displacement this is a positive integer multiple of7, hence at least7. Vectors `(1,2)` and `(-3,1)` attain7. Therefore:

- Same tile diameter: `2r=4/5<1`
- Distinct same-color centers: distance at least `√21r`
- Points in distinct same-color tiles: distance at least `(√21−2)r = 1.033030277982336…>1`

These estimates include closed hexagons. Assigning each boundary point to any one incident tile remains proper.

### Moser spindle

Independently reconstructed the producer's proposed seven points: two unit diamonds `A=(0,0), B=(√3/2,1/2), C=(√3/2,−1/2), D=(√3,0)` rotated by `±θ/2`, where `sin(θ/2)=1/(2√3)`, sharing A, with the far-tip edge added.

All11 specified edges have exact squared distance1. There are no extra unit-distance edges among these seven points. Exhaustive enumeration found:

- 0 proper three-color assignments among `3^7=2187`
- 384 proper four-color assignments

The forcing explanation is correct: each diamond's adjacent middle pair forces its two tips to share the third color; the final tip-to-tip edge contradicts this in a three-coloring. This establishes the elementary lower bound four, not the manuscript's new lower bound six. The historical de Grey result excludes four colors and gives the older lower bound five.

## Script review

Read all13 scenes of `episodes/158/script.json` in both languages. The distinction between unit-distance coloring and map coloring, the equilateral triangle, the Moser lower bound, the classical upper bound, the new claim's unresolved six/seven alternative, and the proof-roadmap attribution are sound within the stated scope.

One important wording clarification was sent to the producer: in the weak-coloring bridge, “product measure” must mean **plane position × unit-circle angular measure**. It must not suggest area measure on `ℝ²×ℝ²`, under which the full set of unit-distance pairs already has measure zero. The manuscript's definition and Lean's `volume.prod angularMeasure` use the correct position-direction measure.

Optional wording note: crossing edges in a particular drawing do not by themselves prove an abstract graph nonplanar. Unit-distance graphs are not required to be planar. The original script did not explicitly make this false inference; the producer was warned not to introduce it.

The 3/4/5-label-cycle roadmap matches the source introduction's lines222–268; it remains only a description of the paper's argument, not a proof supplied by the animation.

## Pending at initial report write

The renderer was still being written. Exact geometry above is verified against the producer's stated coordinates, not yet against final rendered pixels. Final source/render checks and script clarification confirmation will be appended below.

## Renderer/source and frame inspection

Inspected `episodes/158/renderer.py` after it was written, and viewed the actual English Moser, English separation, English transfer-bridge, and Chinese tiling key frames. Confirmed:

- The renderer implements the checked triangular lattice, `(q+3j)%7`, and regular hexagons, with equal x/y scale
- Each Moser diamond remains congruent during rotation; the far-tip edge is only drawn after rotation has reached its exact unit-distance final position
- The separation frame uses enclosing circles for a conservative lower bound, not a false assertion that the nearest polygon vertices lie at the drawn circle extrema
- The weak-coloring subtitle now explicitly says plane-position × unit-circle-direction measure in both languages
- Abstract cycle diagrams are explicitly labeled label relations, not unit-distance graphs

One final notation correction was requested: the Moser diagram originally wrote `A=D₁=D₂` underneath “same tip color”; it should write `c(A)=c(D₁)=c(D₂)` so the displayed equality does not identify distinct vertices. Awaiting confirmation of that small renderer correction before marking final display review closed.

## Final bounded disposition

Both requested corrections are now confirmed in source: the position-direction measure is explicit, and the display reads `c(A)=c(D₁)=c(D₂)`. To avoid relying on a stale preview, I independently rendered the corrected Moser scene at t=18 seconds in both languages using the current renderer, saved the frames under `evidence/158_*_spindle_corrected.png`, and visually checked the English frame. The notation is correct and fits the panel. Source hashes are saved in `evidence/episode158_review_snapshot.json`.

**Mathematical exposition clearance:** the checked source/script/elementary geometry and corrected key-frame content are suitable for the clearly attributed, non-certified educational review animation. This is not independent validation of the new five-color impossibility proof, and not a full final-MP4 decode/quality check. The producer retains responsibility for rendering the corrected source into both final videos.
