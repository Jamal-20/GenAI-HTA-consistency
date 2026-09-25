"""
Compare the N runs field by field.
Flag any field where runs disagree.
Produces results/consistency_table.csv
"""

import pandas as pd
from utils import load_json, values_match


RUNS_PATH = "results/multiple_runs.json"
OUTPUT_PATH = "results/consistency_table.csv"

FIELDS = ["population", "intervention", "comparator", "primary_outcome", "effect_size"]


def main():
    runs = load_json(RUNS_PATH)
    print(f"Loaded {len(runs)} runs.\n")

    rows = []

    for field in FIELDS:
        values = [str(run.get(field, "Not found")) for run in runs]
        first = values[0]
        consistent = all(values_match(v, first) for v in values[1:])

        rows.append({
            "field": field,
            "run_1": values[0],
            "run_2": values[1] if len(values) > 1 else "",
            "run_3": values[2] if len(values) > 2 else "",
            "run_4": values[3] if len(values) > 3 else "",
            "run_5": values[4] if len(values) > 4 else "",
            "consistent": consistent,
            "flag": "FLAG" if not consistent else ""
        })

    df = pd.DataFrame(rows)
    print(df[["field", "consistent", "flag"]].to_string(index=False))
    print()

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved: {OUTPUT_PATH}")

    flagged = df[df["consistent"] == False]["field"].tolist()
    if flagged:
        print(f"\nFlagged fields (needs researcher review): {flagged}")
    else:
        print("\nNo fields flagged. All runs consistent.")
        print("NOTE: If this happens, raise temperature in extract_multiple.py")
        print("to introduce natural variance.")


if __name__ == "__main__":
    main()