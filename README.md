# GenAI in Health Technology Assessment (HTA) Consistency

**Consistency Checks and Evaluation Methodology in LLM-Based HTA Data Extraction**

A focused pilot testing the consistency-checking recommendation from
[Versteeg et al. (2026, *JAMIA Open*)](#references), using a simplified PICO
schema on a single NICE technology appraisal — and surfacing a finding about
**evaluation methodology** that matters for scaling HTA extraction across
jurisdictions.

[![Status](https://img.shields.io/badge/status-pilot%20study-orange)]
[![Schema](https://img.shields.io/badge/schema-PICO%205--field-blue)]
[![Source](https://img.shields.io/badge/source-NICE%20TA1074-green)]
[![License](https://img.shields.io/badge/license-MIT-lightgrey)]

---

## 1. What This Repository Does

This project tests a simplified version of a published recommendation for
LLM-based extraction of Health Technology Assessment (HTA) reports:

&gt; **What happens when a multi-run consistency check produces zero flags — and
&gt; what does that reveal about evaluation methodology?**

Versteeg et al. (2026) extracted 14 attributes from 50 NICE reports and
concluded:

&gt; "Future efforts could study incorporating either multiple extraction runs
&gt; with consistency checks or a researcher-in-the-loop approach, or both."

This repository operationalizes that recommendation on a smaller scale and
arrives at a complementary finding: **evaluation methodology is as important
as model capability.** A naive token-overlap metric marked a *correct*
extraction as wrong because the effect size was expressed as a geometric
LS mean ratio rather than a percentage change — two clinically equivalent
expressions. Semantic evaluation is not optional.

## 2. Research Question

&gt; Can multiple extraction runs with consistency flagging identify errors that a
&gt; single run misses — and what does it mean when the consistency check produces
&gt; no flags because the model is consistently correct?

## 3. Headline Result

| Method | Accuracy | Notes |
|--------|:--------:|-------|
| Single run | **5/5 (100%)** | All fields correctly extracted |
| Multiple runs + consistency check | **5/5 (100%)** | Zero variance across 5 runs |
| After evaluation metric correction | **5/5 (100%)** | Token-overlap metric had produced a false negative |

**Key methodological finding:** a simple token-overlap evaluation metric marked
a *correct* extraction as wrong. The model reported the effect size as a
geometric LS mean ratio (**0.59**, 95% CI 0.51 to 0.69) while the gold standard
was expressed as a percentage change. After correcting the gold standard and
updating the matcher to check for overlapping numbers, the extraction was
validated as correct. This aligns with the Utrecht group's use of
**path-based semantic matching** rather than string matching.

## 4. Honest Positioning

| Aspect | This Project | Versteeg et al. (2026) |
|--------|--------------|------------------------|
| Schema | Simplified 5-field PICO | Full 14-attribute nested schema |
| Reports | 1 NICE report (TA1074) | 50 NICE reports |
| Model | Gemini 3.6 Flash | Claude 3 Opus |
| Focus | Consistency-checking workflow | Full attribute extraction & evaluation |
| Hardest fields (`outcome_rea`, `comparator`) | **Not tested** | ~70% accuracy |

&gt; **This project does not replicate their accuracy results** and does not test
&gt; their hardest fields. It is a *worked example of a specific, diagnosable
&gt; finding about evaluation methodology* — not a benchmark of LLM extraction
&gt; accuracy.

## 5. Why This Matters for Scaling Across Jurisdictions

Versteeg et al. (2026) identified **external validity** as a limitation — NICE
reports only, 14 attributes only, English only — and called for transferability
testing across HTA organisations, languages, and document structures.

This project identifies **evaluation methodology as a critical condition for
scaling:**

| Scaling Challenge | How Semantic Evaluation Addresses It |
|-------------------|--------------------------------------|
| Different document structures across HTA bodies | The same value may be expressed differently in different formats |
| Different languages | Translation may produce different expressions of the same value |
| Multiple medicine–indication combinations per report | More combinations = more potential for cross-attribution errors |
| Regulatory consequences of extraction errors | Correct values must not be marked wrong due to surface differences |

**Core argument:** scaling extraction across jurisdictions is not just a model
problem — it is a **process and evaluation design problem**. A pipeline that
marks correct extractions as wrong will produce an unusable database.

## 6. Method

1. **Gold standard:** manually extracted 5 PICO fields from the
   clinical-effectiveness section of NICE TA1074:
   - Population
   - Intervention
   - Comparator (drug name only)
   - Primary outcome
   - Effect size (numerical ratio)
2. **Prompt design:** structured JSON extraction prompt with explicit
   anti-hallucination rules.
3. **Multi-run extraction:** the same prompt run **5 times** on the same text
   using **Gemini 3.6 Flash** (temperature 0.1), with free-tier-aware pauses
   and exponential backoff.
4. **Consistency check:** compared runs field-by-field; flagged any field
   where runs disagreed.
5. **Simulated researcher-in-the-loop:** for flagged fields, took the majority
   value across runs.
6. **Evaluation:** final output compared against the gold standard using
   accuracy, precision, recall, and F1.
7. **Connection:** findings tied back to Versteeg et al.'s published
   recommendations.

## 7. What This Project Found About Consistency Checking

| Observation | Implication |
|-------------|-------------|
| No variance across 5 runs | Consistency checks detect variance — but cannot detect errors when the model is consistently correct |
| No fields flagged | A researcher-in-the-loop workflow would not be triggered |
| All 5 fields accurately extracted | On a clean, well-structured report with a simplified schema, extraction worked well |
| Evaluation metric produced a false negative | **Evaluation methodology is as important as model capability** |

## 8. Connection to the Utrecht Group's Work

| Versteeg et al. (2026) Finding | This Project |
|--------------------------------|--------------|
| Schema-guided extraction works | Replicated with Gemini 3.6 Flash on a smaller 5-field schema |
| Outcome REA & Comparator hardest (~70%) | Not tested — simplified schema used |
| Reproducibility issues (run-to-run variance) | Not reproduced — perfectly consistent across 5 runs |
| Recommended: multiple runs + consistency checks | Tested; zero flags because zero variance |
| Recommended: researcher-in-the-loop | Tested (simulated); not triggered |
| Semantic evaluation needed | **Confirmed** — token-overlap produced a false negative on a correct extraction |

## 9. Source Document

**NICE Technology Appraisal TA1074** — *Sparsentan for treating primary IgA
nephropathy* (published 25 June 2025).

- Guidance page: &lt;https://www.nice.org.uk/guidance/ta1074&gt;

This repository **does not redistribute NICE's copyrighted report text**.
Download the source document directly from the link above. The `data/` folder
contains a citation file (`source_reference.md`) and the manually constructed
gold standard (`manual_extraction.csv`).

## 10. Repository Structure

hta-genai-consistency/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   ├── manual_extraction.csv        # gold standard, 5 fields
│   └── source_reference.md          # citation + link (no copied report text)
├── prompts/
│   └── extraction_prompt.txt        # the exact prompt used
├── results/
│   ├── multiple_runs.json           # outputs from 5 runs
│   ├── consistency_table.csv        # field-by-field comparison across runs
│   ├── researcher_in_loop.csv       # flagged fields + final values
│   └── comparison_table.csv         # single run vs multi-run + review
├── analysis/
│   ├── error_analysis.md            # error classification and discussion
│   └── hta_context_reflection.md    # connection to published HTA research
└── src/
├── utils.py                     # LLM client, JSON parsing, matching
├── extract_multiple.py          # runs the prompt N times
├── check_consistency.py         # flags fields with disagreement
└── evaluate.py                  # evaluates against gold standard


## 11. Getting Started

### Prerequisites

- Python 3.9+
- A Google Gemini API key

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/hta-genai-consistency.git
cd hta-genai-consistency

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Gemini API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 4. Place the NICE text in data/ta1074_clinical_effectiveness.txt
#    (see data/source_reference.md for instructions)
```

Running the Pipeline
# Run extraction 5 times (~5 API calls, ~1–2 minutes with pauses)
python src/extract_multiple.py

# Check consistency across runs
python src/check_consistency.py

# Evaluate against the gold standard
python src/evaluate.py
#

# 13.  References
| Reference                                      | Link / Description                                                                                                                                                                                               |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Versteeg et al. (2026)                         | *Text mining methods for automated data extraction from health technology assessment reports of medicines using classical natural language processing and generative artificial intelligence.* JAMIA Open, 9(2). |
| NICE TA1074                                    | <https://www.nice.org.uk/guidance/ta1074>                                                                                                                                                                        |
| UtrechtUniversity/health-technology-assessment | <https://github.com/UtrechtUniversity/health-technology-assessment>                                                                                                                                              |
| EU HTA Regulation (EU) 2021/2282               | <https://eur-lex.europa.eu/legal-content/EN/LSU/?uri=CELEX%3A32021R2282>                                                                                                                                         |
