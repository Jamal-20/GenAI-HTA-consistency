# HTA Context Reflection

**Project:** Consistency Checks and Confidence Flagging for Hard-to-Extract HTA Fields

**Purpose:** To connect the findings of this proof-of-concept to the broader HTA research context and the specific needs of the Utrecht University PhD position on Generative AI in Health Technology Assessment.

---

## 1. Why This Project Exists

The Utrecht University PhD position asks:

> "Assessing the extent to which GenAI tools can reliably extract, harmonise, and analyse information from national and EU HTA reports, and identifying the conditions required to scale this across jurisdictions."

The Utrecht University research group (Versteeg et al., 2026, JAMIA Open) published a proof-of-concept showing that LLM-based extraction from HTA reports is feasible and accurate enough for comparative HTA research — but with specific limitations. Their conclusion explicitly recommended two future directions:

1. Multiple extraction runs with consistency checks
2. A researcher-in-the-loop approach (reviewing flagged inconsistencies, validating low-confidence extractions, spot-checking random samples)

This project tests a simplified version of both recommendations on a single NICE report.

---

## 2. The Gap in the Current Evidence Base

| What Versteeg et al. (2026) Did | What They Did Not Do |
|----------------------------------|----------------------|
| Extracted 14 attributes from 50 NICE reports | Test consistency checks across multiple runs |
| Evaluated three methods (rule-based, classification, LLM) | Test a researcher-in-the-loop workflow |
| Documented error rates per attribute | Propose a specific flagging mechanism |
| Recommended future work | Implement that recommendation |

This project addresses that gap at a small scale.

---

## 3. What This Project Found

### Headline Result

| Method | Accuracy | Notes |
|--------|----------|-------|
| Single run | 5/5 (100%) | All fields correct |
| Multiple runs + consistency check | 5/5 (100%) | No variance across runs |
| After evaluation metric correction | 5/5 (100%) | Initial metric produced a false negative |

### Key Finding

The model was perfectly accurate and perfectly consistent. The apparent failure was in the evaluation methodology, not the model. This is important because it shows that:

1. Consistency flagging is useful for detecting variance, but it cannot detect errors when the model is consistently correct (or consistently wrong in the same way).
2. Evaluation metrics must be semantically aware. A token-overlap metric marked a correct clinical effect size as wrong because it was expressed as a ratio rather than a percentage.
3. The Utrecht group's use of semantic evaluation is not optional — it is essential for scaling extraction across jurisdictions where the same value may be expressed differently.

---

## 4. Why This Matters for Scaling Across Jurisdictions

Versteeg et al. (2026) noted that a limitation of their study was external validity — they only used NICE reports, only 14 attributes, and only English. They called for transferability testing across other HTA organisations, languages, and document structures.

**How semantic evaluation helps with scaling:**

| Scaling Challenge | How Semantic Evaluation Addresses It |
|-------------------|----------------------------------------|
| Different document structures across HTA bodies | The same value may be expressed differently in different formats |
| Different languages | Translation may produce different expressions of the same value |
| Multiple medicine-indication combinations per report | More combinations = more potential for cross-attribution errors |
| Regulatory consequences of extraction errors | Correct values must not be marked wrong due to surface differences |

**This is the core argument:** scaling extraction across jurisdictions is not just a model problem — it is a process and evaluation design problem.

---

## 5. Alignment with the Utrecht PhD Position

| Position Requirement | How This Project Addresses It |
|----------------------|-------------------------------|
| "Assessing the extent to which GenAI tools can reliably extract..." | Tested extraction accuracy against a gold standard |
| "...harmonise and analyse information from national and EU HTA reports" | Used a real NICE report; schema aligned with EU HTA attributes |
| "...identifying the conditions required to scale this across jurisdictions" | Identified evaluation methodology as a critical condition for scaling |
| Connection to Versteeg et al. (2026) | Directly tested their recommended future work |
| Use of LLMs for extraction and analysis | Used Gemini 3.6 Flash |

---

## 6. What a Larger-Scale Version Would Look Like

If extended to a full PhD project, this work could involve:

| Extension | Rationale |
|-----------|-----------|
| 50+ reports across NICE, ZIN, and EU JCA | Test transferability across jurisdictions |
| 14 attributes (matching Versteeg et al.) | Enable direct comparison of findings |
| Real human reviewers (not simulated) | Measure true researcher-in-the-loop performance |
| Multiple LLM providers | Test model dependence of the flagging mechanism |
| Semantic evaluation metrics | Move from token overlap to clinically aware matching |
| Integration with existing HTA workflows | Move from proof-of-concept to practice |

---

## 7. Broader HTA Implications

**For HTA bodies:**

Automated extraction could reduce the time and cost of comparative HTA research. But the value depends on trust. A semantically aware evaluation ensures that correct extractions are not marked wrong due to surface differences — which makes the automated process auditable and defensible.

**For researchers:**

An Open Science database of extracted HTA attributes (as the Utrecht group is building) becomes more reliable if evaluation is semantically aware. Downstream analyses can trust that values were not incorrectly excluded.

**For policymakers:**

Cross-border HTA collaboration (under the EU HTA Regulation) requires comparable data. Semantic evaluation provides a mechanism for recognising when data are equivalent even when expressed differently — which is essential for comparability.

---

## 8. Personal Reflection

Building this project gave me firsthand understanding of why the Utrecht group's recommendation for semantic evaluation matters. I saw that a correct extraction could be marked wrong by a simple string-matching metric, and that consistency checks alone do not catch this kind of evaluation error. This convinced me that the hard problem in GenAI for HTA is not just model capability, but evaluation and process design — and that is the problem I want to work on in a PhD.

---

## 9. References

| Reference | Link/Description |
|-----------|------------------|
| Versteeg et al. (2026) | Text mining methods for automated data extraction from health technology assessment reports of medicines using classical natural language processing and generative artificial intelligence. JAMIA Open, 9(2). |
| NICE TA1074 | https://www.nice.org.uk/guidance/ta1074 |
| UtrechtUniversity/health-technology-assessment | GitHub repository |
| EU HTA Regulation (EU) 2021/2282 | https://eur-lex.europa.eu/legal-content/EN/LSU/?uri=CELEX%3A32021R2282 |