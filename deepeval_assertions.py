from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric
)

from deepeval.test_case import LLMTestCase


def run_deepeval(response_data):

    metric_relevancy = AnswerRelevancyMetric(
        threshold=0.7
    )

    metric_faithfulness = FaithfulnessMetric(
        threshold=0.7
    )

    test_case = LLMTestCase(
        input=response_data["question"],
        actual_output=response_data["answer"],
        retrieval_context=response_data["contexts"]
    )

    relevancy_score = metric_relevancy.measure(test_case)
    faithfulness_score = metric_faithfulness.measure(test_case)

    print(f"Relevancy Score: {relevancy_score}")
    print(f"Faithfulness Score: {faithfulness_score}")

    assert relevancy_score >= 0.7
    assert faithfulness_score >= 0.7
