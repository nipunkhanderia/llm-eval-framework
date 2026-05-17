# ============================================================
# evaluator/report_generator.py
# ============================================================
# PURPOSE:
#   Takes evaluation results and:
#   1. Prints a detailed summary to the terminal
#   2. Saves a CSV report to the /reports folder
#
# WHY CSV THIS TIME (not text like Project 1):
#   CSV files can be opened in Excel.
#   In real QA work, stakeholders want to see results in
#   spreadsheets — not text files.
#   This is more professional and interview-ready.
# ============================================================

import os
import csv
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


def print_evaluation_result(result: dict):
    """
    Prints one evaluation result to the terminal in a readable format.

    Parameters:
        result : A dict containing all evaluation data for one prompt
                 (built in main.py)
    """
    print("\n" + "=" * 65)
    print(f"  [{result['id']}] {result['category']}")
    print("=" * 65)

    # Show the prompt (truncated)
    print(f"\n📝 PROMPT: {result['prompt'][:80]}{'...' if len(result['prompt']) > 80 else ''}")

    # Show response (truncated)
    if result["success"]:
        print(f"🤖 RESPONSE: {result['response'][:150]}{'...' if len(result['response']) > 150 else ''}")
        print(f"⏱️  LATENCY: {result['latency']}s")
    else:
        print(f"❌ CALL FAILED: {result['error']}")
        return

    print(f"\n📊 DIMENSION SCORES:")
    print("-" * 65)

    # Print each dimension score with colour
    for score in result["dimension_scores"]:
        bar = "█" * (score["score"] // 10) + "░" * (10 - score["score"] // 10)

        if score["score"] >= 75:
            colour = Fore.GREEN
        elif score["score"] >= 50:
            colour = Fore.YELLOW
        else:
            colour = Fore.RED

        print(f"  {score['dimension']:<15} {colour}{bar} {score['score']:>3}/100{Style.RESET_ALL}")
        print(f"  {'':15} └── {score['details'][:70]}")

    print("-" * 65)

    # Total score and grade
    total = result["total_score"]
    grade = result["grade"]
    passed = result["passed"]

    if passed:
        result_str = f"{Fore.GREEN}PASSED ✅  {grade}{Style.RESET_ALL}"
    else:
        result_str = f"{Fore.RED}FAILED ❌  {grade}{Style.RESET_ALL}"

    print(f"\n  TOTAL SCORE: {total}/100  →  {result_str}")
    print("=" * 65)


def save_csv_report(all_results: list):
    """
    Saves all evaluation results to a CSV file.
    CSV can be opened directly in Excel.

    Parameters:
        all_results : List of result dicts, one per test case

    Returns:
        The file path where the CSV was saved
    """
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = f"reports/eval_report_{timestamp}.csv"

    # Define the columns in our CSV
    fieldnames = [
        "ID", "Category", "Prompt",
        "Relevance", "Safety", "Fluency", "Conciseness", "Factuality",
        "Total Score", "Grade", "Passed", "Latency (s)", "Response Preview"
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for r in all_results:
            if not r["success"]:
                continue

            # Extract individual dimension scores into a lookup dict
            scores = {s["dimension"]: s["score"] for s in r["dimension_scores"]}

            writer.writerow({
                "ID": r["id"],
                "Category": r["category"],
                "Prompt": r["prompt"],
                "Relevance":   scores.get("Relevance", "N/A"),
                "Safety":      scores.get("Safety", "N/A"),
                "Fluency":     scores.get("Fluency", "N/A"),
                "Conciseness": scores.get("Conciseness", "N/A"),
                "Factuality":  scores.get("Factuality", "N/A"),
                "Total Score": r["total_score"],
                "Grade":       r["grade"],
                "Passed":      "YES" if r["passed"] else "NO",
                "Latency (s)": r["latency"],
                "Response Preview": r["response"][:100] + "..."
            })

    return filepath


def print_final_summary(all_results: list, csv_path: str):
    """
    Prints a final summary table after all test cases are evaluated.

    Parameters:
        all_results : List of all result dicts
        csv_path    : Path where the CSV report was saved
    """
    successful = [r for r in all_results if r["success"]]
    passed = [r for r in successful if r["passed"]]
    failed = [r for r in successful if not r["passed"]]

    print("\n" + "🏁 " * 20)
    print("   FINAL EVALUATION SUMMARY")
    print("🏁 " * 20)

    print(f"\n  Total Test Cases : {len(all_results)}")
    print(f"  ✅ Passed        : {len(passed)}")
    print(f"  ❌ Failed        : {len(failed)}")

    if successful:
        avg_score = round(sum(r["total_score"] for r in successful) / len(successful))
        avg_latency = round(sum(r["latency"] for r in successful) / len(successful), 2)
        print(f"  📊 Average Score : {avg_score}/100")
        print(f"  ⏱️  Avg Latency   : {avg_latency}s")

    print(f"\n  📁 CSV Report saved to: {csv_path}")
    print("  (Open the CSV in Excel to see full results)\n")
