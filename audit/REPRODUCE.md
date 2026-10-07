# Reproduce the bounded original checks

Use Python 3.12 and install `audit/requirements.txt`. From the project root:

```sh
python audit/audit_math_checks.py
python audit/check_episode158.py
```

These print their results. Compare with `audit/evidence/independent-checks.json` and `audit/evidence/episode158_geometry.json`. These finite arithmetic and elementary geometry tests do not verify the manuscript's complete research claims. No Lean build was performed. The upstream Fourier verifier is not copied here; its pinned source path and recorded hashes/output are described in `REPORT.md`.
