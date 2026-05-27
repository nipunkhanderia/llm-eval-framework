from datasets import Dataset

from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy
)


def run_ragas(response_data):

    dataset = Dataset.from_dict({
        "question": [response_data["question"]],
        "answer": [response_data["answer"]],
        "contexts": [response_data["contexts"]],
        "ground_truth": [
            "pytest is a Python testing framework."
        ]
    })

    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy
        ]
    )

    print(result)

    assert result["faithfulness"] >= 0.7
    assert result["answer_relevancy"] >= 0.7
