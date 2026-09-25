"""
Run the same extraction prompt N times on the same text.
Free-tier friendly: adds a pause between calls and retries on quota errors.
Produces results/multiple_runs.json
"""

import os
import sys
import time
from utils import call_llm, extract_json_from_text, load_text, save_json


N_RUNS = 5
DELAY_BETWEEN_RUNS = 15   # seconds; increase if you hit free-tier limits
REPORT_PATH = "data/ta1074_clinical_effectiveness.txt"
PROMPT_PATH = "prompts/extraction_prompt.txt"
OUTPUT_PATH = "results/multiple_runs.json"


def main():
    if not os.path.exists(REPORT_PATH):
        print(f"ERROR: {REPORT_PATH} not found.")
        print("Please extract the clinical-effectiveness section of NICE TA1074")
        print("and save it as plain text in data/.")
        sys.exit(1)

    report_text = load_text(REPORT_PATH)
    prompt_template = load_text(PROMPT_PATH)
    prompt = prompt_template.replace("{TEXT}", report_text)

    print(f"Running {N_RUNS} extractions with {DELAY_BETWEEN_RUNS}s delay...")
    print(f"Report length: {len(report_text)} characters\n")

    runs = []
    for i in range(1, N_RUNS + 1):
        print(f"Run {i}/{N_RUNS}...", end=" ", flush=True)
        try:
            # Slight temperature variation to expose run-to-run variance
            # If all runs are identical, raise this value (e.g. 0.3)
            temp = 0.1
            raw = call_llm(prompt, temperature=temp)
            parsed = extract_json_from_text(raw)
            if parsed is None:
                print("FAILED TO PARSE")
                parsed = {"error": "parse_failed", "raw": raw[:500]}
            else:
                print("OK")
            parsed["_run"] = i
            parsed["_temperature"] = temp
            runs.append(parsed)

        except Exception as e:
            print(f"ERROR: {e}")
            runs.append({"_run": i, "error": str(e)})

        # Polite pause between runs to stay within free tier
        if i < N_RUNS:
            print(f"  (pausing {DELAY_BETWEEN_RUNS}s for free-tier limits...)")
            time.sleep(DELAY_BETWEEN_RUNS)

    save_json(runs, OUTPUT_PATH)
    print(f"\nSaved {len(runs)} runs to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()