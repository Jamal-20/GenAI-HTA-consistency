# Error Analysis

**What the model got right, what went wrong, and where the error actually was.**

---

## 1. Summary

| Metric | Single Run | Multi-Run + Review |
|--------|------------|--------------------|
| Correct fields | 5 / 5 | 5 / 5 |
| Accuracy | 100% | 100% |
| Fields flagged | 0 | 0 |

---

## 2. Field-Level Outcomes

| Field | Gold Standard | Extracted | Correct? |
|-------|---------------|-----------|----------|
| Population | Adults with biopsy-confirmed IgA nephropathy and persistent proteinuria despite ≥12 weeks of maximally tolerated RASi therapy | adults with biopsy-confirmed primary IgAN and persistent proteinuria despite at least 12 weeks of stable, maximum RASi therapy | Yes |
| Intervention | Sparsentan | sparsentan | Yes |
| Comparator | Irbesartan | irbesartan | Yes |
| Primary Outcome | Percentage change in UPCR from baseline to week 36 | percentage change in UPCR from baseline to week 36 | Yes |
| Effect Size | Geometric LS mean ratio 0.59 (95% CI 0.51 to 0.69) | geometric LS mean ratio 0.59 (95% CI 0.51 to 0.69) | Yes |

**No model errors were found.**

---

## 3. Evaluation Error (Not a Model Error)

| Item | Detail |
|------|--------|
| **Type** | Evaluation false negative |
| **Field** | `effect_size` |
| **What happened** | Initial token-overlap metric marked the field wrong |
| **Why** | Gold standard included both the ratio (0.59) and the percentage change (−49.8% vs −15.1%). Model extracted only the ratio. Both are clinically equivalent. |
| **Fix** | Gold standard updated to primary effect size; matching function updated to check for overlapping numbers |

---

## 4. Consistency Flagging

| Field | Flagged? | Correct? |
|-------|----------|----------|
| Population | No | — |
| Intervention | No | — |
| Comparator | No | — |
| Primary Outcome | No | — |
| Effect Size | No | — |

| Metric | Count |
|--------|-------|
| True positives | 0 |
| False positives | 0 |
| False negatives | 0 |
| True negatives | 5 |

**Interpretation:** No flags because there was no variance. Consistency
checking catches variance — it cannot catch errors when the model is
consistently correct (or consistently wrong in the same way).

---

## 5. Run-to-Run Variance

| Field | Distinct Values | Substance of Variance |
|-------|-----------------|------------------------|
| Population | 2 | Capitalisation only |
| Intervention | 2 | Capitalisation only |
| Comparator | 2 | Capitalisation only |
| Primary Outcome | 2 | Capitalisation only |
| Effect Size | 2 | Capitalisation only |

All variance was superficial. Semantic content was identical across runs.

---

## 6. Connection to Versteeg et al. (2026)

| Their Finding | This Project |
|---------------|--------------|
| Outcome REA and Comparator are hardest (~70%) | Not tested — simplified schema |
| Reproducibility issues | Not reproduced — model was consistent |
| Recommended: consistency checks | Tested — no flags (no variance) |
| Recommended: researcher-in-the-loop | Tested — not triggered |
| Semantic evaluation needed | Confirmed — token overlap produced a false negative |

---

## 7. Limitations

- Single report, single therapy area
- Simplified 5-field schema (not Versteeg et al.'s 14 attributes)
- 5 runs — enough to show consistency, not to estimate accuracy
- Simulated researcher-in-the-loop (majority vote)
- Single LLM provider (Gemini 3.6 Flash)

---

## 8. Conclusion

The model performed perfectly. The error was in the evaluation metric, not
the model. This is a worked example of why **semantic evaluation** — not
simple string matching — is necessary for scaling extraction across
jurisdictions. It confirms a point Versteeg et al. also make in recommending
a path-based semantic matching algorithm.
