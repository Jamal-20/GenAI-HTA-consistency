# HTA Context Reflection

**How this project connects to Versteeg et al. (2026) and the Utrecht GenAI-HTA project.**

---

## 1. Why This Project Exists

The Utrecht PhD position asks how far GenAI can reliably extract, harmonise, and
analyse HTA report data — and what conditions are needed to scale that across
jurisdictions.

Versteeg et al. (2026, *JAMIA Open*) showed extraction is feasible but recommended
two next steps:

1. Multiple extraction runs with consistency checks
2. A researcher-in-the-loop approach

This project tests a simplified version of both on one NICE report.

---

## 2. What This Project Actually Did

| Aspect | This Project | Versteeg et al. (2026) |
|--------|--------------|------------------------|
| Schema | Simplified 5-field PICO | Full 14-attribute nested schema |
| Reports | 1 (NICE TA1074) | 50 NICE reports |
| Model | Gemini 3.6 Flash | Claude 3 Opus |
| Focus | Consistency-checking workflow | Full extraction + evaluation |

**This is a focused pilot, not a replication.** It does not test their hardest
fields (`outcome_rea`, full comparator structure). It tests the
consistency-checking recommendation using a smaller schema.

---

## 3. What It Found

| Method | Accuracy |
|--------|----------|
| Single run | 5/5 (100%) |
| Multi-run + consistency check | 5/5 (100%) |
| After evaluation metric correction | 5/5 (100%) |

The model was accurate and consistent. **No fields were flagged** — because
there was no variance.

**Key finding:** A token-overlap metric marked a *correct* extraction as wrong.
The effect size was expressed as a geometric LS mean ratio (0.59, 95% CI
0.51–0.69), which is clinically equivalent to the percentage change also
reported. Simple string matching cannot see that equivalence.

---

## 4. Why This Matters for Scaling

Versteeg et al. noted their study was limited to NICE reports, English, and 14
attributes. They called for transferability testing.

Scaling across jurisdictions means:

- Different document structures
- Different languages
- Different ways of expressing the same value

A pipeline that marks correct extractions as wrong will produce an unusable
database. **Evaluation methodology is part of the scaling problem — not a
detail.**

This aligns with the Utrecht group's use of a **path-based semantic matching
algorithm** rather than simple string comparison.

---

## 5. What a Larger Version Would Look Like

| Extension | Why |
|-----------|-----|
| 50+ reports across NICE, ZIN, EU JCA | Test transferability |
| 14-attribute schema (matching theirs) | Enable direct comparison |
| Real human reviewers (not simulated) | Measure true researcher-in-the-loop |
| Semantic evaluation metrics | Move beyond token overlap |

---

## 6. References

- Versteeg et al. (2026). *JAMIA Open*, 9(2).
- NICE TA1074. https://www.nice.org.uk/guidance/ta1074
- EU HTA Regulation (EU) 2021/2282
