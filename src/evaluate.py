"""
Evaluate single-run and multi-run+review outputs against gold standard.
Produces results/researcher_in_loop.csv and results/comparison_table.csv.
"""

import pandas as pd
from collections import Counter
from utils import load_json, values_match


GOLD_STANDARD = {
    "population": "Adults with biopsy-confirmed IgA nephropathy and persistent proteinuria despite at least 12 weeks of maximally tolerated RASi therapy",
    "intervention": "Sparsentan",
    "comparator": "Irbesartan",
    "primary_outcome": "Percentage change in UPCR from baseline to week 36",
    "effect_size": "Geometric LS mean ratio 0.59 (95% CI 0.51 to 0.69)"
}

FIELDS = list(GOLD_STANDARD.keys())


def evaluate_values(values_by_field: dict) -> dict:
    correct = 0
    rows = []
    for field in FIELDS:
        extracted = values_by_field.get(field, "Not found")
        gold = GOLD_STANDARD[field]
        is_correct = values_match(extracted, gold)
        rows.append({
            "field": field,
            "gold": gold,
            "extracted": extracted,
            "correct": is_correct
        })
        if is_correct:
            correct += 1
    return {
        "rows": rows,
        "correct": correct,
        "total": len(FIELDS),
        "accuracy": correct / len(FIELDS)
    }


def main():
    runs = load_json("results/multiple_runs.json")
    consistency = pd.read_csv("results/consistency_table.csv")

    print("=" * 70)
    print("EVALUATION: Single Run vs Multiple Runs + Researcher Review")
    print("=" * 70)

    # --- 1. Single run (baseline) ---
    single_run = {field: runs[0].get(field, "Not found") for field in FIELDS}
    single_eval = evaluate_values(single_run)

    # --- 2. Multiple runs + simulated researcher review ---
    reviewed = {}
    for field in FIELDS:
        values = [str(run.get(field, "Not found")) for run in runs]
        is_flagged = not consistency.loc[
            consistency["field"] == field, "consistent"
        ].iloc[0]

        if is_flagged:
            counts = Counter(values)
            reviewed[field] = counts.most_common(1)[0][0]
        else:
            reviewed[field] = values[0]

    reviewed_eval = evaluate_values(reviewed)

    # --- 3. Comparison table ---
    print("\nField-by-field comparison:")
    print("-" * 70)
    rows = []
    for field in FIELDS:
        s = next(r for r in single_eval["rows"] if r["field"] == field)
        r = next(r for r in reviewed_eval["rows"] if r["field"] == field)
        rows.append({
            "field": field,
            "single_run": "CORRECT" if s["correct"] else "WRONG",
            "multi_run_reviewed": "CORRECT" if r["correct"] else "WRONG",
        })
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

    # --- 4. Summary ---
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Single run accuracy:       {single_eval['correct']}/{single_eval['total']} "
          f"({single_eval['accuracy']*100:.0f}%)")
    print(f"Multi-run + review:        {reviewed_eval['correct']}/{reviewed_eval['total']} "
          f"({reviewed_eval['accuracy']*100:.0f}%)")

    # --- 5. Save researcher-in-the-loop detail ---
    rl_rows = []
    for field in FIELDS:
        values = [str(run.get(field, "Not found")) for run in runs]
        is_flagged = not consistency.loc[
            consistency["field"] == field, "consistent"
        ].iloc[0]
        gold = GOLD_STANDARD[field]
        final = reviewed[field]
        rl_rows.append({
            "field": field,
            "flagged": is_flagged,
            "run_values": " | ".join(values),
            "final_value": final,
            "gold": gold,
            "final_correct": values_match(final, gold)
        })

    rl_df = pd.DataFrame(rl_rows)
    rl_df.to_csv("results/researcher_in_loop.csv", index=False)
    df.to_csv("results/comparison_table.csv", index=False)

    print("\nSaved:")
    print("  results/researcher_in_loop.csv")
    print("  results/comparison_table.csv")


if __name__ == "__main__":
    main()