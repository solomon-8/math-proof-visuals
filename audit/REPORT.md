# OpenAI math：有限范围独立审计

审计对象：`https://github.com/openai/math`，固定提交 `adc7f1241b42e322a6451854ab7e4b4c146bf78a`。审计日期：2026-10-07 UTC。仓库只读，工作树仍干净。

## 结论先行

**本轮没有确认一条“数学陈述不成立”或“足以推翻主要结论的证明错误”。这不是全仓证明正确的结论。**

本轮完成了三种不同强度的检查：

1. 形式化边界与命题核对，重点是组017的 π 无理性指数。论文、独立 Comparator 目标与主 Lean 命题对应，最后的指数桥接未见明显缺口。但没有运行 Lean，也没有逐行认证深层插值论证
2. 一个非 Lean 计算证书的真实重跑：六阶复 Hadamard/Fourier 论文的标准库 Python 精确有理数验证器成功完成，退出码0，输出与论文规定一致
3. 四组独立有限代数检查：π 数值例子、S4 永久式证明的协方差恒等式、十维仿射极大图的 ODE/不变盒代数、三边缘 Coulomb 反例的中心 Hessian 计算，以及 Hadamard 两个显式样本。都通过；这些检查不能替代原论文的普遍性与渐近论证

没有把 challenge 文件中的 `sorry`、没有安装编译器、或目录 review=`unchecked` 当作定理错误。没有将未找到反例表述为证明成立。

## 1. 仓库与验证范围

顶层 README 说明有722篇手稿、372个成果组，验证程度不同，未形式化结果可能存在问题。库存核对显示：

- `preprints/` 的722个目录与 README 一致
- `lean/formalization.yaml` 包含162篇 source、185条 main-result 记录，对应178个不同的 Comparator 配置
- 实际有405个 Comparator JSON 文件，配置允许的公理均为 `propext`、`Quot.sound`、`Classical.choice`
- 该 YAML 自述 `Partial progress`，review 为 `unchecked`
- **162是较窄清单的稿件数，不是“全仓只有162篇有形式化”或“162篇已逐项独立复核”的计数。** 例如 PiExponent 不在这份 YAML 内，但有独立说明、挑战、配置与 solution

详见 `lean-boundaries/report.md`、`inventory.json` 和 `audit_inventory.py`。

## 2. 组017：μ(π)=2，可用于有清楚归属的教育说明

### 已核内容

论文 `preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/paper.pdf` 第1页 Theorem 1.1；源文件 `build/main.tex:50–78`；`lean/ComparatorChallenges/PiExponent.lean:7–15`；`lean/OAI/NumberTheory/PiExponent/Main.lean:17–27` 表达同一实质命题：

对每个实数 ν>2，存在整数 Q≥2，使每个整数 p 及每个整数 q≥Q 满足

|π−p/q| ≥ q^(−ν)

同时，以无限多个约分有理数的逼近误差定义的指数上确界等于2。Comparator 的目标直接使用 Mathlib 的 `Real.pi` 和有理数分母，没有靠改名定义将结论变成别的命题。主入口没有把“μ(π)=2”作为假设。

`Approximation/Exponent.lean:7–106` 明确处理整数/自然数分母转换、有限分母集合、Dirichlet 无限逼近、ν>2的逼近集合有限、实数上确界的非空及有界性。最后这段桥接未见明显逻辑遗漏。深层插值和解析命题在 `Main.lean` 处由实际 theorem 提供，不是未填的结构参数；869个本地 OAI 导入文件的文本扫描未发现实际 `axiom/sorry/admit` 声明。

### 必须保留的界限

- Q依赖ν，论文不有效给出它
- 不表示所有分数的误差≥1/q²，也不推出固定正数c的c/q²下界
- 尚未认证所有869个文件的数学语义、外部库、编译过程或完整证明
- Flint–Hills 收敛不属于此 Comparator 选中的目标；但 `Main.lean:29–32` 另有该定理，不应误说仓库没有它

独立90位精度数值核对：

- |π−22/7| ≈ 0.0012644892673496186802；q²误差≈0.06195997410013131533
- |π−355/113| ≈ 0.00000026676418906242231237；q²误差≈0.00340631193013807051

两者都小于1/q²。这只纠正错误解读，不是论文定理的反例。

### 视频脚本复核

已读 `episodes/017/SCRIPT_REVIEW.md` 的中英文稿。鸽巢段、量词段、非零行列式/清分母段及中心无关阈值段，与正文 `main.tex:158–240` 的自述对应。建议鸽巢段显式写 `1≤q≤N`。允许表述：

> 仓库声称证明 μ(π)=2，并提供针对该完整命题的 Lean 源码与 Comparator 配置。本次核对了命题和量词对应，尚未独立验证整套证明。

不能据本次审计声称“已独立跑通 Lean”“已获数学界确认”。

## 3. 真正运行的精确证书：六阶复 Hadamard / Fourier

论文目录：`preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/`。不在 YAML 的162篇 source中。

先检查 `README.md`、`verification/run.py` 及 `verify.py`：纯标准库组合枚举、整数/有理数运算、断言检查，没有网络、安装或外部命令。wrapper 校验脚本 SHA-256 并拒绝关闭断言的执行模式。随后按 README 执行：

`python -u …/verification/run.py`

退出码：0。完整输出：

    rank table: 8871 909 897
    rank table: 46041 3429 2767
    -613302797399911/6480 179721388988719/6480 5000000000000000

脚本 SHA-256：`104a7306205b8544c8f913f6afdb59603f2e04a207c9ac592c383b80eb0e2aa9`，与 wrapper 中固定值一致。

实际检查内容包括：模运算寻找候选线性代换后，以整数/有理数回代验证；单矩阵非负式恒等于零；六个 Gram 矩阵精确正定；混合式剩余常数与系数绝对值和相加严格为负。正文对应 `build/sections/05-verification.tex`，特别是:369–396。

**强度界限：代码重跑通过证明该明确有限计算按所给程序成立，不自动认证全部“几何/概率语义→线性关系”的翻译。** 已查看单矩阵 moment 定义及消元解释，转置对称并非未经许可假设：定义确实平均 H 和 H^T。未逐个独立重建全部混合矩关系和完整 MUB 结论。

另用独立脚本在精确圆分域内核对：F6 的 Gram 矩阵与全部20种α字符为零；Tao 的显式矩阵及其逐项平方均为 Hadamard。都通过，仅为样本检查。

证据：`evidence/fourier-verifier.log`。

## 4. 非形式化证明的可控代数检查

### 4.1 四行永久式与 Thorp shuffle

目录 `A-strict-four-row-permanent-inequality-and-permutation-moments-September-26-2026`，PDF第3–5页；`build/sections/02-permanent.tex`。

针对局部不等式关键项，枚举全部85个取值于{-2,-1,0,1,2}且均值零的四维行向量，检查7225对向量在全部24个S4排列上的精确有理数协方差：

E[g(π(1))h(π(2))] = −〈g,h〉/3

全部通过，与 Eq.(4) 的二次项上界和 p>4/3 局部阈值一致。人工核对其确切均匀边缘假设、从局部缺口到紧性延伸、Lemma2.1张量化，未见明显遗漏。

未完整审计后面的表示论、多重度、稀疏停止、树递推及最终 O(log N) 混合结论。不要把这个测试说成验证了 Thorp 主定理。

### 4.2 十维光滑非二次仿射极大图

目录 `Smooth-Nonquadratic-Affine-Maximal-Graph-in-Dimension-Ten-October-5-2026`，PDF第5–6页 Lemmas4.1–4.2；源文件 `build/source/main.tex:318–427`。

独立符号运算从 A、B、C 系统重新求 D=C/B 的微分方程，与 Eq.(16) 一致；精确核对盒顶点(9/2,7/2,33/7)是平衡点及六个边界表达式。上边界方向分别由 B≤7/2、22A+84D≤495、7A+3B≤42直接给出非正；下边界方向为0、0、11A。未发现符号错误。

人工阅读径向局部固定点、延拓边界和 Hessian 正性逻辑；此轮不作为 PDE 主定理的完整认证，未运行数值 PDE 或形式化。

### 4.3 三边缘 Coulomb 的 Monge 不达最小值

目录 `A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026`，PDF第3–8页，特别 Lemma2.1、Lemma3.1、Proposition4.1。

检查重点为“任意 Borel map”而非仅某一类规则映射的质量障碍。论证用每个选择集S的像满足 μ(H(S))=ν(S)/6，而 μ(S)=ν(S)/3；额外原像只会加重矛盾，未见把总质量误当逐点选择的漏洞。

独立取K=20，在中心(0,e1,−e1)精确计算 Hessian。M+20I正定，两个隐函数导数块行列式为2025/7784746与1/3892373，均非零；不同方向中心的成本余量为(√2−1)/2>0。这支持原文“足够大的K”及局部支撑构造。对称的e2情形相同。

K不是任意正数；例如较小K的导数退化不能反驳其“足够大”存在性陈述。本轮没有拿不满足条件的参数制造反例。未完整独立验证第6–7节的所有推广与 infima 逼近。

## 5. 阅读筛选但没有完成认证的内容

- `Ultraflat-real-Littlewood-polynomials-October-5-2026`：阅读主定理、舍入、辅助函数和波形拼接。涉及依赖其他手稿的 signed interval packing；未重建其完整证明，也未产生满足原文条件的反例
- `A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026`：阅读 Faber 系数、正核、两个有序乘法测试及正块矩阵比较。未见可立即证伪的低维代数断言；未进行完整独立审定
- `A-counterexample-to-Sidorenkos-conjecture-September-23-2026`：仅初筛主定理、结构及有限域/奇异配置依赖。没有完成50余页证明审计，不能据此评价主结论
- Mahler 与特征2 Kaplansky：只做选定形式化目标与局部导入边界抽查，细节见子报告；没有完整 PDF 对照或编译
- 所有其他手稿未作逐项数学审计

## 6. Lean 执行限制与下一步

本环境没有 PATH 可用的 `lean`、`lake`、`elan`、`comparator`、`lean4export`、`landrun`，没有该 checkout 的 `.lake`，也未发现常见工具链目录。仓库固定 Lean `v4.34.1`，Lake manifest 有42个依赖包记录。

`lakefile.lean:262–275` 在配置 elaboration 阶段已有 `run_cmd`，其依赖准备函数会 clone/patch（clone 在:243–245）。所以不能把 `lake env` 当作无副作用的简单探测。此轮没有安装、下载、运行 Lake 或改动仓库。

外部工具链/缓存尚未下载，**无法从本地文件可靠给出所需下载或解压体积**，不提供虚假的估值。最小数学入口是 `ComparatorChallenges/PiExponent.json`；准备好可信、隔离且依赖齐全的环境后，按 `lean/ComparatorChallenges/README.md` 的方式运行专属 Comparator，而不是编译整个库。运行前仍须检查依赖兼容补丁与验证器版本。

建议下一轮明确二选一：以017的完整 Comparator 运行作为终点；或将一个非形式化结果的全部关键引理与外部引用作完整人工审计。本轮证据不足以给722篇全仓的正误保证。

## 7. 复现和证据

- 独立数学检查：`python audit_math_checks.py`；结果 `evidence/independent-checks.json`
- 精确证书真实输出：`evidence/fourier-verifier.log`
- 静态库存/导入：`python lean-boundaries/audit_inventory.py`，结果同目录
- π第一页面渲染、命题文字比较、工具状态：`lean-boundaries/`
- 辅助PDF文字提取：`text/`；断言以PDF及LaTeX源为准，避免因提取丢失上划线/根号制造误报

所有输出位于仓库外；未改动待审仓库。

## 附录：第158与107集教育脚本审核（2026-10-07后续）

此后按限定视频范围，新增了源命题、双语脚本、renderer及关键帧审查，未扩大全仓扫描或执行Lean。

- 158：独立精确核对Moser七点十一条unit边、三色穷举零解、四色384解；证明所用七色格最近同色中心距与点距下界1.03303027798；实际renderer几何及关键帧对应。修正弱染色“位置×方向测度”措辞、同色公式`c(A)=c(D₁)=c(D₂)`。详见 `episode158_review.md`、`check_episode158.py`和evidence
- 107：核对复数域`ω≤9/4`与每个ε>0的有限无除法程序`Oε(n^(9/4+ε))`；核对张量/共享腿/5M副本、M输出块、每块M维辅助点积及谱增长叙述。修正M=3 Fourier示意里极端失配格本应缺席的问题，补明`t=t(λ)>0`与程序模型；复看源及关键帧通过。详见 `episode107_review.md`

两集当前版本在已查范围内可作为“明确归属原论文、未独立认证新证明”的教育审稿动画。图示修订不是原仓库定理错误的发现。最终完整MP4解码/声音/字幕同步检验由制作任务另行完成；此审计不覆盖它们。


## 公开副本说明

本副本保留原审查结论及限制。PDF全文抽取、临时页面图像和机器专属日志未公开；原始论文可按文中固定提交链接获取。部分静态库存脚本和大体量导入图仅留作当次检查记录，未计入公开可复现脚本；公开的独立算术/几何测试及短结果位于本目录。
