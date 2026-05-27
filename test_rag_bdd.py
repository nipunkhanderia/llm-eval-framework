from pytest_bdd import (
    scenarios,
    given,
    when,
    then,
    parsers
)

from app.rag_pipeline import ask_rag

from tests.deepeval_assertions import run_deepeval
from tests.ragas_assertions import run_ragas


scenarios("features/rag.feature")


@given(
    parsers.parse('a user asks "{question}"'),
    target_fixture="question"
)
def user_question(question):
    return question


@when(
    "the RAG system generates a response",
    target_fixture="response_data"
)
def generate_response(question):
    return ask_rag(question)


@then("the response should pass DeepEval metrics")
def validate_deepeval(response_data):
    run_deepeval(response_data)


@then("the response should pass Ragas metrics")
def validate_ragas(response_data):
    run_ragas(response_data)
