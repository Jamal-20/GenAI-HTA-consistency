# Error Analysis

**Project:** Consistency Checks and Confidence Flagging for Hard-to-Extract HTA Fields

**Source document:** NICE Technology Appraisal TA1074 — Sparsentan for treating primary IgA nephropathy (published 25 June 2025)

**Model used:** Gemini 3.6 Flash

**Number of runs:** 5

**Gold standard fields:** population, intervention, comparator, primary_outcome, effect_size

---

## 1. Summary of Results

| Metric | Single Run | Multi-Run + Researcher Review |
|--------|------------|-------------------------------|
| Correct fields | 5 / 5 | 5 / 5 |
| Accuracy | 100% | 100% |
| Fields flagged for review | 0 | 0 |

---

## 2. Field-Level Outcomes

| Field | Gold Standard | Extracted Value | Correct? | Flagged? |
|-------|---------------|-----------------|----------|----------|
| Population | Adults with biopsy-confirmed IgA nephropathy and persistent proteinuria despite ≥12 weeks of maximally tolerated RASi therapy | adults with biopsy-confirmed primary IgAN and persistent proteinuria despite at least 12 weeks of stable, maximum RASi therapy | Yes | No |
| Intervention | Sparsentan | sparsentan | Yes | No |
| Comparator | Irbesartan | irbesartan | Yes | No |
| Primary Outcome | Percentage change in UPCR from baseline to week 36 | percentage change in UPCR from baseline to week 36 | Yes | No |
| Effect Size | Geometric LS mean ratio 0.59 (95% CI 0.51 to 0.69) | geometric LS mean ratio 0.59 (95% CI 0.51 to 0.69) | Yes | No |

---

## 3. Error Classification

### Model Errors

**No model errors were found.** All five fields were correctly extracted in all five runs.

### Evaluation Error Identified

- **Error type:** Evaluation false negative
- **What happened:** The initial token-overlap metric marked the `effect_size` field as wrong because the gold standard included both the ratio (0.59, 95% CI 0.51–0.69) and the percentage change values (−49.8% vs −15.1%), while the model extracted only the ratio.
- **Why it happened:** The gold standard was overly inclusive, and the token-overlap threshold (50%) was too strict for clinically equivalent expressions of the same effect size.
- **How it was corrected:** The gold standard was updated to the primary effect size (geometric LS mean ratio 0.59, 95% CI 0.51 to 0.69), and the matching function was updated to check for overlapping numbers before falling back to token overlap.

---

## 4. Consistency Flagging Performance

| Field | Flagged? | Was the Flag Correct? |
|-------|----------|------------------------|
| Population | No | — |
| Intervention | No | — |
| Comparator | No | — |
| Primary Outcome | No | — |
| Effect Size | No | — |

**Flagging metrics:**

- True positives: 0
- False positives: 0
- False negatives: 0
- True negatives: 5

**Interpretation:** The consistency check produced no flags because the model was perfectly consistent across all 5 runs. This means consistency flagging did not detect any errors — because there were none. However, it also means consistency flagging would not have detected an error if the model had been confidently wrong in the same way across all runs.

---

## 5. Run-to-Run Variance

| Field | Distinct Values | Most Common Value | Runs with Most Common Value |
|-------|-----------------|-------------------|------------------------------|
| Population | 2 (case-only difference) | lowercase version | 3 / 5 |
| Intervention | 2 (case-only difference) | lowercase version | 3 / 5 |
| Comparator | 2 (case-only difference) | lowercase version | 3 / 5 |
| Primary Outcome | 2 (case-only difference) | lowercase version | 3 / 5 |
| Effect Size | 2 (case-only difference) | lowercase version | 3 / 5 |

**Observation:** All variance was superficial (capitalisation only). The semantic content was identical across all runs. No substantive variance was observed.

---

## 6. Connection to Published Literature

Versteeg et al. (2026, JAMIA Open) reported:

- Overall accuracy of 88–98% for 12 of 14 attributes
- "Outcome relative effectiveness" and "Comparator" were the hardest fields (~70% accuracy)
- Reproducibility issues were a noted limitation
- Their conclusion recommended multiple extraction runs with consistency checks and a researcher-in-the-loop approach

**How your findings align:**

| Their Finding | Your Finding | Alignment |
|---------------|--------------|-----------|
| Outcome REA and Comparator are hardest | Effect size extracted correctly | Does not confirm |
| Reproducibility issues | No substantive variance | Does not confirm |
| Multiple runs + consistency checks recommended | Consistency check produced no flags | Not tested (no errors to catch) |
| Researcher-in-the-loop recommended | Not triggered | Not tested |

**Discussion:** This project did not reproduce the failure modes documented by Versteeg et al. The model performed perfectly on this single report. This may be because Gemini 3.6 Flash is a newer model than Claude 3 Opus used in their study, or because TA1074 is a relatively clean report with a well-defined primary endpoint. The key finding of this project is methodological: evaluation metrics matter. A simple token-overlap metric produced a false negative on a correct extraction.

---

## 7. Limitations of This Analysis

- Single report, single therapy area (nephrology)
- Five runs — enough to demonstrate consistency, not to estimate a reliable error rate
- Simulated researcher-in-the-loop (majority vote), not a real human reviewer
- Single LLM provider (Google Gemini); results may differ with other models

---

## 8. Conclusion

The model extracted all five PICO fields correctly and consistently. The consistency check produced no flags because there was no variance. The key finding is that an overly strict evaluation metric produced a false negative on a correct extraction. This demonstrates that evaluation methodology is as important as model capability for scaling extraction across jurisdictions — and it aligns with the Utrecht group's use of semantic evaluation rather than simple string matching.