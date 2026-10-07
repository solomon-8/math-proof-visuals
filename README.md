# Math Proof Visuals · 数学论证可视化

Bilingual visual explainers of mathematical claims, with explicit source attribution and verification limits.

中英双语数学视频：讲清命题、量词和关键思路，同时标明来源与核验边界。

## Production status · 制作进度

As of 7 October 2026 UTC:

- Episodes 017, 158 and 107 each have separate Chinese/English subtitle-only review cuts completed locally
- Narrated videos for all three episodes are awaiting a new voice (`awaiting_new_voice`)
- The previous Kokoro voice was rejected by the user. Its audio, voiced MP4s, and release package are not published
- A new model/voice sample must be approved by the user before full narration or voiced publication resumes
- All other result families in the 372-family queue remain pending
- The repository contains the 017 review source, the 372-family research catalogue and ranking, and bounded review evidence. Further episode source and approved downloads are added as their publication checks finish

Counts: 372 result families in total; 3 bilingual subtitle-only review cuts ready; 369 families pending video production; 0 approved narrated episodes. These production counts are separate from the files published in this repository.

No claim is made that all 372 source result families have videos or independently verified proofs.

## Research and review · 研究与审查

- [Research report and communication ranking](research/REPORT.md), [complete 372-family ranking](research/ranking.json), and [attributed catalogue](research/catalog.json)
- [Algorithms and practical-computing scope](research/algorithms.md), [physics and real-world relevance](research/physics.md)
- [Sources and precise scope for the first three episodes](research/FIRST_THREE_SOURCES.md)
- [Bounded proof-review report](audit/REPORT.md), [Episode 158 mathematical review](audit/episode158_review.md), [Episode 107 mathematical review](audit/episode107_review.md)
- [Reproduce the editorial ranking](research/REPRODUCE.md), [reproduce the bounded original checks](audit/REPRODUCE.md), [machine-readable production status](production_status.json)

The editorial ranking is a production queue, not a probability that a proof is correct. The audit found no confirmed mathematical counterexample within its bounded checks; it does not certify the full repository.

## Episode 017 · How close can a fraction get to π?

**Status: subtitle-only review animatic, without narration or music.** This explains the claim made by the source manuscript. It is not an independent certification of its proof, a successful Lean build, or evidence of peer-review acceptance.

**当前为无配音、无音乐的字幕审稿样片。** 本片讲解来源论文的主张；不代表独立认证了整份证明，也未独立编译其 Lean 工程。

The episode introduces rational approximations, denominator-dependent error, the irrationality exponent, the pigeonhole argument, and the distinction between every exponent ν > 2 and the endpoint ν = 2. Numerical examples and diagrams illustrate the ideas; they do not prove the new manuscript claim.

The manuscript's claim is: for every real ν > 2, there is a threshold Q(ν) such that every integer p and every integer q ≥ Q(ν) satisfy |π − p/q| ≥ q^(−ν). The threshold depends on ν. This does not give a uniform c/q² bound or an explicit numerical threshold.

## Files

- `episodes/017/script.json`: bilingual scene content and timing
- `episodes/017/subtitles/017.zh.srt`, `017.en.srt`: Chinese and English subtitles
- `video/render.py`: original Pillow/NumPy/Matplotlib animation renderer
- `video/validate.py`: checks encoded streams, full decoding, numerical examples and text bounds
- `episodes/017/metadata.json`: provenance, review status and video checksums
- `scripts/render.sh`: creates output folders and invokes the renderer
- `requirements.txt`: pinned direct Python dependencies used for rendering
- `licenses/` and `THIRD_PARTY_NOTICES.md`: source and font notices
- `SOURCE_SNAPSHOT.md`: pinned source and proof-status boundaries

Finished MP4 files are distributed separately from the source tree. Published download links must be added after upload and verification; this source snapshot does not imply that a GitHub Release exists.

## Reproduce the visuals

The tested rendering environment used Python 3.12.14, Pillow 12.3.0, NumPy 2.3.5, Matplotlib 3.10.8, and FFmpeg 7.1.5 on Debian Linux. FFmpeg must include the `libx264` encoder. The current renderer uses the Debian locations for DejaVu Sans and Noto Sans CJK fonts.

On a Debian/Ubuntu machine, install the system dependencies yourself as appropriate:

```sh
sudo apt-get update
sudo apt-get install python3 python3-venv ffmpeg fonts-dejavu-core fonts-noto-cjk
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Generate a quick frame preview (both languages):

```sh
sh scripts/render.sh --language both --frames-only
```

Render both videos at 24 fps:

```sh
sh scripts/render.sh --language both --fps 24
```

Outputs are written under `episodes/017/frames/`, `episodes/017/renders/`, and `episodes/017/subtitles/`. `--language en` or `--language zh` renders one language. The renderer regenerates subtitle files. Rendered MP4 files have no audio track. Different dependency, font, or encoder builds can produce different bytes; this is a reproducible source workflow, not a promise of bit-identical output.

To check locally rendered MP4s after both languages finish:

```sh
mkdir -p video/qa
python video/validate.py
```

The validator regenerates subtitles and decoded sample frames, and writes `video/qa/validation.json`. Its passed result tests the media and illustrative numbers, not the validity of the complete research proof.

## Source and attribution

Source: OpenAI, *The irrationality exponent of π is 2*, 24 September 2026, in `openai/math`, snapshot `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

- [Source manuscript](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/paper.pdf)
- [Source README and citation](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/README.md)
- [Formalization scope](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/017.md)
- [Comparator configuration](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/PiExponent.json)

Original explanatory visuals, script paraphrases, and commentary are distinct from the upstream manuscript. This project is not an official OpenAI release or endorsement. Third-party notices do not automatically license all new project material; see `THIRD_PARTY_NOTICES.md`.
