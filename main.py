# ============================================================
# main.py
# ============================================================
# PURPOSE:
#   Entry point for the LLM Evaluation Framework.
#   Runs every test case through llama3.2 and scores each one.
#
# HOW TO RUN:
#   python main.py
#
# WHAT HAPPENS:
#   1. Loads all test cases from prompts/test_dataset.py
#   2. Sends each prompt to llama3.2 via Ollama
#   3. Scores each response across 5 dimensions
#   4. Prints results to terminal
#   5. Saves a CSV report to /reports folder
# ============================================================

from evaluator.llm_caller import call_llm
from evaluator.scorer import (
    score_relevance,
    score_safety,
    score_fluency,
    score_conciseness,
    score_factuality,
    calculate_total_score
)
from evaluator.report_generator import (
    print_evaluation_result,
    save_csv_report,
    print_final_summary
)
from prompts.test_dataset import TEST_DATASET


def evaluate_single_prompt(test_case: dict) -> dict:
    """
    Runs the complete evaluation pipeline for ONE test case.

    Steps:
        1. Call llama3.2 with the prompt
        2. Score the response across 5 dimensions
        3. Calculate total score
        4. Return everything as one result dict

    Parameters:
        test_case : One entry from TEST_DATASET

    Returns:
        A complete result dictionary with all scores
    """

    print(f"\n⏳ Evaluating [{test_case['id']}]: {test_case['prompt'][:60]}...")

    # Step 1: Call the LLM
    llm_result = call_llm(test_case["prompt"])

    # Step 2: If the call failed, return early with failure info
    if not llm_result["success"]:
        return {
            "id": test_case["id"],
            "category": test_case["category"],
            "prompt": test_case["prompt"],
            "success": False,
            "error": llm_result["error"],
            "response": "",
            "latency": llm_result["latency"],
            "dimension_scores": [],
            "total_score": 0,
            "grade": "F — Failed",
            "passed": False
        }

    response = llm_result["response"]

    # Step 3: Score across all 5 dimensions
    dimension_scores = [
        score_relevance(
            prompt=test_case["prompt"],
            response=response,
            expected_keywords=test_case["expected_keywords"]
        ),
        score_safety(response),
        score_fluency(response),
        score_conciseness(
            response=response,
            ideal_min=test_case["ideal_min_words"],
            ideal_max=test_case["ideal_max_words"]
        ),
        score_factuality(
            response=response,
            known_false_claims=test_case.get("known_false", [])
        ),
    ]

    # Step 4: Calculate weighted total score
    total = calculate_total_score(dimension_scores)

    # Step 5: Combine everything into one result dict
    return {
        "id": test_case["id"],
        "category": test_case["category"],
        "prompt": test_case["prompt"],
        "success": True,
        "error": None,
        "response": response,
        "latency": llm_result["latency"],
        "dimension_scores": dimension_scores,
        "total_score": total["total_score"],
        "grade": total["grade"],
        "passed": total["passed"]
    }


def main():
    """
    Main function — evaluates all test cases and generates report.
    """
    print("\n" + "🚀 " * 20)
    print("   LLM EVALUATION FRAMEWORK — STARTING")
    print(f"   Model: llama3.2 via Ollama")
    print(f"   Test Cases: {len(TEST_DATASET)}")
    print("🚀 " * 20)

    all_results = []

    # Loop through every test case in our dataset
    for i, test_case in enumerate(TEST_DATASET, start=1):
        print(f"\n{'─' * 65}")
        print(f"  TEST {i} of {len(TEST_DATASET)}")
        print(f"{'─' * 65}")

        # Run evaluation for this test case
        result = evaluate_single_prompt(test_case)
        all_results.append(result)

        # Print result to terminal
        print_evaluation_result(result)

    # Save CSV report
    csv_path = save_csv_report(all_results)

    # Print final summary
    print_final_summary(all_results, csv_path)


if __name__ == "__main__":
    main()
