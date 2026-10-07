# Mathematical physics shortlist: careful explanations

Snapshot inspected: OpenAI `math`, HEAD `adc7f1241b42e322a6451854ab7e4b4c146bf78a` (verified locally). Research date: 2026-10-07 UTC. Read-only review of the repository; no build, upload, or external-state change performed. PDF statements, introductions, proof overviews, Lean scope documents, actual solution entry points, and comparator specifications inspected. This is a scope/evidence assessment, not a peer review or an independently rerun formal verification.

## Recommendation

Choose **362, relativistic Vlasov–Maxwell global regularity**, and **269, the unperturbed Laughlin spectral gap**, if the selection balances foundational significance, relevance to physics, and direct formalization coverage. These are distinct large advances in nonlinear dynamics and quantum many-body theory. Present them as results claimed in this release, with accompanying formalization artifacts, rather than as already independently certified by this review.

**265, area laws and PEPS**, is the best alternative if the editorial priority is a recognizable connection to computational methods. Its relevance to tensor networks is unusually direct, but it has no accompanying formalization in this snapshot and its PEPS theorem explicitly disclaims an efficient algorithm. **271, ferromagnetic ordering**, is the easiest everyday-physics explainer and has a formalized core, but the newer Bloch-law companions go beyond the documented Lean coverage. **376, forced-fluid computation**, is striking foundational computability rather than an engineering advance.

## Evidence labels to preserve

- “The manuscript proves/claims X” reports the paper's mathematical assertion
- “Lean artifacts cover X” reports repository scope, with an actual solution module and comparator specification inspected
- Neither statement means this review compiled and checked X, audited every definition and dependency, or established independent expert acceptance
- The repository README explicitly says results are at different verification stages and unformalized results may have issues
- `sorry` in `ComparatorChallenges/*.lean` marks the *challenge statement*, not automatically an incomplete solution. The solution module is specified by the corresponding JSON. The selected solution entry points contain proofs and import substantial libraries
- The Vlasov–Maxwell, Heisenberg, Laughlin and LaughlinGap solution directories were searched for literal `sorry`, `admit`, and `axiom`; no matches were returned. This is a limited textual check, not a substitute for kernel checking or an audit of their transitive dependencies
- The comparator JSON files inspected permit `propext`, `Quot.sound`, and `Classical.choice`, and have `enable_nanoda: false`. No comparator run was performed

## 1. Family 362: no finite-time breakdown in a specified plasma model

### 中文解释

**可以用来讲什么：** 给定一团带电粒子的初始分布，粒子产生电磁场，电磁场又改变粒子的运动，两者不断相互反馈。问题是：即使开始时十分平滑，这种反馈会不会在有限时间内把数学解推到失控、无法继续的程度？这篇论文声称，在所研究的三维相对论性单一粒子种类、无碰撞模型中，只要初始数据满足明确的光滑性、能量和支撑条件，就不会出现这种有限时间的经典解崩溃，而且演化是唯一的。

**为什么重要：** 这是给一个基础动力学模型补上长期缺失的“方程可以一直一致地演化下去”的数学保证。早先的小数据、特殊对称情形、以及较弱意义下的解，和这里对任意大小的合格光滑数据的经典解结论并不相同。关键进展是去掉小振幅和对称性限制。

**实际意义应怎样说：** 它加强等离子体数学模型的基础，也可能为后续的稳定性分析和数值误差分析提供工具。这些是合理的研究方向推断；论文本身没有展示更快的模拟器、实验改进、聚变装置优化或工业落地。全局光滑不等于长期行为简单，也不等于误差不会增长。

**简短安全版本：** “这项结果声称证明了：在一类严格规定的三维无碰撞等离子体模型中，任意大小的合格光滑初始数据都会产生全局唯一的光滑演化。它解决的是模型是否会在有限时间内失去经典解的问题，而不是直接给出聚变工程方案。”

### English explanation

Charged particles create electromagnetic fields, which push the particles in return. The manuscript claims that this feedback cannot cause finite-time loss of a classical solution in the specified three-dimensional relativistic one-species collisionless model, for arbitrary-size admissible smooth initial data. This would settle a major foundational well-posedness problem. It is not a numerical speedup or a demonstrated plasma-control technology.

### Exact theorem and restrictions

Source: manuscript Theorem 1.1, pp. 2–3; Lean `docs/362.md`; `ComparatorChallenges/VlasovMaxwell.lean`; solution `OAI/Analysis/VlasovMaxwell/Main.lean` and model definitions.

- Spatial domain is all of R³; momentum also ranges over R³
- Relativistic particle velocity is v/sqrt(1+|v|²). The system is collisionless Vlasov coupled to Maxwell
- **One species; no background charge**. Do not silently generalize to a multi-species, collisional, bounded-container, or relativistic-gravity plasma
- Initial density f₀ is nonnegative, C∞, and compactly supported in **both position and momentum**
- E₀ and B₀ are C∞ with every spatial derivative bounded; fields themselves belong to L² (finite field energy)
- Gauss compatibility holds: div E₀ = ∫f₀dv and div B₀ = 0
- There is no smallness, symmetry, or neutrality assumption. Nonzero total charge and a Coulomb tail are allowed. All field derivatives need not be L²
- The conclusion is a unique global classical solution, smooth on every finite time interval, with compact particle phase-space support on every finite horizon
- The classical comparison class includes C¹ solutions, time-continuous L² fields, and compact particle support on finite horizons
- **Not** a uniform-in-time bound: the momentum-support bound can grow with the chosen finite horizon

### Why the proof is nontrivial

The established continuation route asks for bounded particle momentum on finite intervals. The manuscript's proposed new ingredient is a bound on **signed momentum increments**, taking the norm after integration of the Lorentz force, rather than simply integrating its absolute magnitude. It exploits cancellation in retarded electromagnetic interactions, energy flux, and bounds on how long particles occupy certain geometric regions. The resulting lower bounds on the time needed for momentum doublings have a divergent sum. This is the mechanism claimed to rule out infinite momentum growth in finite time. Describe this as the manuscript's strategy, not as a complete proof supplied by the explainer.

### Verification scope

This is an unusually close match between headline and formal target: the actual `global_classical_solution` target includes admissibility, global classical existence, finite-horizon smoothness, and uniqueness in the specified class. The solution `Main.lean` proves that target using imported continuation and momentum-increment results. The Vlasov–Maxwell package contains 207 Lean source files. File count establishes substantial artifacts, not correctness by itself.

### Realistic impact

- Direct mathematical value: removes a major conditional foundation for this model, if the full result withstands checking
- Plausible future value: new nonlinear PDE estimates and improved foundations for stability/approximation analysis
- No established industrial payoff in the inspected material
- Do not call it “solving Navier–Stokes,” “all plasma equations,” “a fusion breakthrough,” or “an algorithm predicting any plasma forever”

### Source pointers

- [Manuscript, Theorem 1.1 and proof strategy](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026/paper.pdf)
- [Lean scope](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/362.md)
- [Actual solution entry point](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/OAI/Analysis/VlasovMaxwell/Main.lean)
- [Comparator configuration](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/VlasovMaxwell.json)
- Independently retrieved prior work: [Wei–Yang, large Maxwell fields with small particle density](https://arxiv.org/abs/2005.06130); [Wang, cylindrically symmetric large data](https://arxiv.org/abs/2203.01199). These support the distinction between earlier restricted results and the release's claim; they do not validate the new proof

## 2. Family 269: a nonvanishing excitation cost for the Laughlin model

### 中文解释

**可以用来讲什么：** 一个量子体系的基态，是能量最低的状态。“有能隙”是说，要离开基态、产生激发，必须付出一笔最低能量。对宏观物理真正重要的是：体系越来越大时，这笔最低能量会不会越来越接近零？这篇论文声称，对填充因子为 1/3 的特定 Laughlin 模型，即使粒子数不断增加，激发能量仍有一个与粒子数无关的正下界。

**为什么重要：** Laughlin 波函数是分数量子霍尔效应理论的核心对象之一。知道某个波函数恰好是最低能态，还不足以说明它与激发态之间始终隔着一段能量。这个结果补的是后一环，因此会加强对这一理想化量子相的数学理解。

**限制必须一起讲：** 定理针对最低朗道能级内、圆球几何上的完整 V₁ 赝势模型，填充为 1/3；它不是对任意电子材料、一般库仑相互作用或所有分数量子霍尔态的定理。数值 1/25 使用论文自己的相互作用归一化，不能直接换成某个器件的电子伏特或工作温度。

**简短安全版本：** “这项结果声称证明了一个经典量子多体模型的激发能隙不会随着系统增大而消失，为理解 1/3 Laughlin 态提供了严格基础。仓库的 Lean 材料覆盖未加扰动的能隙；同一组论文中关于弱无序稳定性的进一步结论，不能一并称为已形式化。”

### English explanation

A spectral gap is a minimum energy cost for exciting a quantum system out of its ground state. The important issue is whether that cost stays positive as the system grows. The release claims a size-independent lower bound for the full spherical fermionic V₁ Laughlin model at filling 1/3. This would supply a central missing piece of rigorous theory for that idealized fractional-quantum-Hall model. It is not a proof of a useful operating temperature or a fault-tolerant quantum device.

### Exact unperturbed theorem

Source: *A Fock-space inequality and the Laughlin spectral gap*, Theorem 1.1 and Corollary 1.2, pp. 1–2; `docs/269.md`; actual Laughlin and LaughlinGap solution modules.

- One-particle space U_Q is the lowest Landau level on a round sphere with flux Q, equivalently spin Q/2
- Antisymmetric N-particle states describe fermions
- H_{N,Q} is the sum over all unordered pairs of projectors onto pair total spin Q−1, i.e. relative angular momentum one
- Each pair projector has coefficient one, with **no N- or Q-dependent rescaling**
- The full V₁ interaction is retained; this is not the orbital-truncated or thin-cylinder version
- On the whole lowest-Landau-level Fock space, for each 0 < γ < γ* = 4616733319001/10¹⁴ ≈ 0.0461673, H_Q² ≥ γH_Q for all sufficiently large Q, with threshold independent of particle number
- At Laughlin flux Q = 3(N−1), the unique zero-energy ground state is the cubic Laughlin state, and H_{N,Q} ≥ (1/25)(I−P_L) for all sufficiently large N
- The large-size threshold is **existential**, not an explicit certified N₀. The finite-sphere theorem does not claim the endpoint γ* itself
- In a different particle sector with no zero mode, H² ≥ γH bounds energy away from zero; it is **not automatically** a gap between that sector's lowest two eigenvalues
- The manuscript also treats a planar homogeneous-sector endpoint inequality. Keep the main explanation on the spherical filling-1/3 statement unless the added scope is needed

### What the disorder companion adds, and what is not formalized

*Uniform Stability of the Spherical Laughlin Gap*, Theorem 1.1, p. 3, claims constants λ*>0, Δ*>0 and N* such that, for all N≥N*, all bounded measurable real scalar potentials φ with ||φ||∞≤1 on the physical round sphere, and |λ|≤λ*, the **projected one-body perturbation** λ∑ᵢΠφΠ leaves a unique ground state and gap at least Δ*. Constants are independent of N and φ and are existential. Sphere radius is sqrt(q/2), magnetic length is one, and q=3(N−1).

The ground state may move under perturbation and its energy is subtracted. This is not simply bounding a fixed many-body perturbation by a small global operator norm: the total one-body norm can grow with N. **The scope document explicitly excludes disorder stability and perturbed ground-state uniqueness from its selected Lean statement.** Do not attach the Lean label to those further claims.

### Why the proof is interesting

The proposed proof compares H² with a positive sum built from a finite set of annihilation-operator patterns. Rotational symmetry reduces pieces to manageable angular-momentum blocks; rational certificates check finite inequalities. The essential infinite-size step bounds errors **relative to the interaction energy**, rather than by an absolute operator norm that grows with particle number. This yields a bound uniform over particle sectors. The actual formalization contains finite certificates and the passage to the global bound; it is not just a numerical diagonalization for a few particles.

### Verification scope

- `LaughlinGap/Main.lean` proves the 1/25 `MainTarget`, explicitly assembled from finite certificates
- `ComparatorChallenges/LaughlinGap.lean` spells out the energy, antisymmetry, cubic Laughlin polynomial, and squared distance to its line; its target is the eventual 1/25 inequality
- An additional older `Laughlin/Main.lean` target gives 1/100. The documentation reports both; do not mistake 1/100 for a contradiction or claim only that weaker bound is represented
- Additional comparator targets cover Fock-space and planar inequalities
- This review inspected artifacts and their scope but did not build them or establish independent mathematical acceptance

### Realistic impact

The direct result is rigorous control of an important idealized quantum many-body phase. The stable-gap picture is relevant to understanding robustness, but the inspected material does not supply a materials recipe, a Coulomb-model theorem, quantum-computing hardware, or a performance improvement. Any device-level inference would require substantial additional physics and engineering.

### Source pointers

- [Gap manuscript](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-Fock-space-inequality-and-the-Laughlin-spectral-gap-September-24-2026/A-Fock-space-inequality-and-the-Laughlin-spectral-gap-September-24-2026.pdf)
- [Disorder-stability manuscript](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Uniform-Stability-of-the-Spherical-Laughlin-Gap-October-5-2026/uniform-stability-spherical-laughlin-gap.pdf)
- [Lean scope and limitations](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/269.md)
- [1/25 solution entry point](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/OAI/Analysis/LaughlinGap/Main.lean)
- [Precise comparator statement](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/LaughlinGap.lean)
- Independently retrieved background: [Rougerie, *On the Laughlin function and its perturbations*](https://arxiv.org/abs/1906.11656), especially Appendix A. It identifies the model spectral-gap question and its place in rigorous FQHE theory; it does not validate this release's proof

## Other three families: editorial and technical cautions

### 271. Spontaneous magnetization; Bloch law companions

**Good Chinese hook:** “为什么没有外加磁场时，许多量子自旋仍能在低温下自发选定一个方向？” The mathematical advance is establishing ordered equilibrium for an idealized model, not discovering that magnets exist.

**Formalized core:** On Zᵈ for every d≥3 and every S=1/2,1,3/2,…, the nearest-neighbor isotropic quantum Heisenberg ferromagnet with coupling one has, at all sufficiently low positive temperatures, a translation-invariant zero-field β-KMS state with magnetization at least S/4. Threshold β₀(d,S) is finite but not presented as a practical critical-temperature prediction. The theorem asserts an **existence of a chosen ordered state**; averaging its rotations can remove the one-point magnetization. It is not a statement that every equilibrium state is magnetized. The manuscript explicitly distinguishes this from the cited finite-volume two-point order criterion.

**Newer claims:** For the 3D finite-range model, J(z)≥0, J(z)=J(−z), J(0)=0, and the support of J generates Z³. At fixed positive spin and fixed coupling, the claimed Bloch coefficient is

lim_{β→∞} β^{3/2}[S−m_{S,J}(β)] = ζ(3/2)/(8π^{3/2} sqrt(det D_{S,J})), with D_{S,J}=(S/2)∑_zJ(z)zzᵀ.

The order of limits is volume→∞, then positive field→0, then temperature→0. The first lattice correction is a separate nearest-neighbor result. **The Lean scope page covers spontaneous magnetization and convergence of the dynamics, not these Bloch-law, lattice-correction, or spherical-law companions.** Do not conflate the family heading with coverage of every paper.

**Actual inspected sources:** *Spontaneous magnetization…*, Theorem 1.1 pp. 2–3; *Bloch's Law for Finite-Range…*, Theorem 1.1 p. 2; `lean/docs/271.md`; `ComparatorChallenges/Heisenberg.{lean,json}`; `OAI/MathematicalPhysics/Heisenberg/Main.lean`. In Lean ℓ=2S, so the bound ℓ/8 is S/4.

**Useful external background:** [Correggi–Giuliani–Seiringer, free-energy spin-wave theorem](https://arxiv.org/abs/1312.7873) concerns free-energy asymptotics. A free-energy result alone is not a proof of spontaneous magnetization or of the required one-sided field derivative.

### 265. Area law and polynomial PEPS approximation

**Good Chinese hook:** “一个量子系统虽然包含海量自由度，其基态跨越一个区域边界的纠缠，是否只随边界长度增长，而不是随区域面积增长？如果还能把整个状态压缩成适中的张量网络，计算物理就有了更坚实的表示基础。”

**Area-law statement:** For every finite induced square-lattice domain Λ (holes and disconnected pieces allowed), fixed on-site dimension q, induced-graph interaction range R, interaction norm bound J, unique ground vector Ω, and fixed **full-system** spectral gap Δ>0, S_Ω(A)≤C(q,R,J,Δ)|∂_ΛA| for every A⊆Λ. There is at most one summand per support, giving a uniform local interaction-count bound. The same C is independent of domain size/shape and region. No gap is required for restrictions to subregions.

**PEPS statement:** Open L×L square, fixed q≥2, bounded on-site and nearest-neighbor Hermitian terms ||h||≤J, unique ground state, full gap Δ. There exist C,c depending only on q,J,Δ and a nonzero PEPS on the same grid with bond dimension ≤CLᶜ and normalized global vector error ≤L⁻¹ up to phase. No translation invariance, frustration-freeness, commutativity, or gapped path from a product state is required.

**Critical limit:** The PEPS manuscript p. 3 explicitly makes **no claim that tensors can be found or contracted efficiently**; entries can depend arbitrarily on H and Ω. A polynomial-size representation is not a polynomial-time simulator. The companion also explains why a von Neumann area law alone is insufficient for arbitrary states; extra compatible-approximation arguments matter. Do not imply the entropy bound immediately supplies the algorithm.

**Evidence:** Two substantial manuscript PDFs (area-law and PEPS); no `lean/docs/265.md`, no family Lean link, and no corresponding entry found in `formalization.yaml`. Rank as a major unformalized claim in this snapshot. The potential computational relevance is high, but immediate industrial impact is unsubstantiated.

**Sources:** `preprints/A-two-dimensional-area-law-from-a-global-spectral-gap-September-24-2026/paper.pdf`, Theorem 1.1 p. 3; `preprints/Polynomial-PEPS-approximation-of-gapped-square-grid-ground-states-September-24-2026/paper.pdf`, Theorem 1.1 pp. 3–4.

### 376. Universal computation in specially forced fluids

**Good Chinese hook:** “精心设计外力，可以让一条理想流体粒子的轨迹模拟程序；粒子是否最终进入指定区域，与程序是否停机等价。因此，一般性的无限时间轨迹判断会遭遇停机问题。”

**Representative particle theorem:** On the fixed unit flat three-torus and any fixed positive **computable** viscosity, a terminating compiler maps a Turing machine and finite input to a finite effective smooth force program. The fluid starts at rest. A fixed labeled particle reaches a fixed open detector iff the machine halts. The chosen velocity is globally smooth and unique within the stated classical comparison class. In the *Fixed Particle Test* version, every mixed force/velocity derivative is bounded and square-integrable in time in spatial supremum norm. Force can additionally be made divergence-free. No efficient running-time bound is promised.

**Other variants:** The eventual-stationarity companion has force independent of time for t≥1, bounded mixed derivatives, and uniformly bounded kinetic energy. The Lean scope also covers rapidly decaying forces, velocity-field detectors, sheet programs, and whole-box transport, including a fixed-particle construction in R³ starting at (4,0,0), detector (−1,2)³, common compact support and force f₀+νf₁, periodic after time one. Do not combine different papers' properties into a single stronger theorem without checking their statement.

**Most important cautions:** The forcing is specifically engineered to realize prescribed smooth flows. This is **not** the general 3D Navier–Stokes existence-and-smoothness problem. Exact real-coordinate encoding supplies unbounded information; the manuscripts explicitly deny a uniform finite-precision perturbation tolerance for arbitrarily long computations, and deny an efficient simulation-time bound. It is not evidence that an ordinary turbulent fluid is a useful computer, or that normal engineering simulations are impossible.

**Evidence:** Substantial Lean coverage exists, but the scope page explicitly says the sheet-program statement does not include the associated paper's fixed-particle detector or reciprocal solid-box maps; later listed formal targets cover other fuller detector and box results. The eventual-stationarity manuscript is not among the four accompanying papers named by that scope page. Keep exact paper-target pairing.

**Sources:** *A Fixed Particle Test for Computation in a Forced Viscous Flow*, pp. 1–3; *Universal Computation with Eventually Stationary Navier–Stokes Forcing*, pp. 1–2; `lean/docs/376.md`; `ComparatorChallenges/ForcedNavierStokesComputation.{lean,json}` and other comparator links listed there.

## Suggested one-line ranking rationale

“362 和 269 最适合作为兼顾基础意义与形式化覆盖的重点；265 最有张量网络计算的潜在关联，但仍需核查未形式化的证明；271 最容易用日常物理解释；376 展示的是可计算性的理论边界，不能当成纳维–斯托克斯千禧年难题或实用流体计算机的突破。”

## URL provenance

The repository remote is `https://github.com/openai/math.git`. Immutable source links above are built from that verified origin, the verified snapshot commit, and existing file paths; they were not separately fetched over the web in this review. Public external background links were retrieved with web search and are primary papers or author surveys. Background searches were not an exhaustive search for later expert responses to this release.
