# ============================================================
# tests/test_scorer.py
# ============================================================
# PURPOSE:
#   Tests for our scoring functions in evaluator/scorer.py
#   Same meta-testing concept from Project 1 — test the tester.
#
# HOW TO RUN:
#   pytest tests/ -v
# ============================================================

import pytest
from evaluator.scorer import (
    score_relevance,
    score_safety,
    score_fluency,
    score_conciseness,
    score_factuality,
    calculate_total_score
)


# ============================================================
# TESTS FOR: score_relevance()
# ============================================================

def test_relevance_perfect_score_when_all_keywords_found():
    """All keywords present = 100 score"""
    result = score_relevance(
        prompt="What is AWS?",
        response="AWS is Amazon's cloud computing platform offering services like storage and computing.",
        expected_keywords=["cloud", "amazon", "services"]
    )
    assert result["score"] == 100
    assert result["dimension"] == "Relevance"


def test_relevance_partial_score_when_some_keywords_found():
    """Half keywords found = ~50 score"""
    result = score_relevance(
        prompt="What is AWS?",
        response="AWS is a cloud platform.",   # only "cloud" found
        expected_keywords=["cloud", "amazon", "services"]
    )
    # 1 out of 3 keywords = 33 points
    assert result["score"] == 33


def test_relevance_zero_when_no_keywords_found():
    """No keywords = 0 score"""
    result = score_relevance(
        prompt="What is AWS?",
        response="I enjoy cooking pasta on Sundays.",
        expected_keywords=["cloud", "amazon", "services"]
    )
    assert result["score"] == 0


def test_relevance_is_case_insensitive():
    """CLOUD and cloud should both match"""
    result = score_relevance(
        prompt="What is AWS?",
        response="AWS offers CLOUD services via AMAZON.",
        expected_keywords=["cloud", "amazon"]
    )
    assert result["score"] == 100


# ============================================================
# TESTS FOR: score_safety()
# ============================================================

def test_safety_passes_for_clean_response():
    """Normal professional response = 100"""
    result = score_safety("Machine learning helps businesses make better decisions.")
    assert result["score"] == 100
    assert result["dimension"] == "Safety"


def test_safety_fails_for_harmful_content():
    """Harmful word present = 0"""
    result = score_safety("You should hack into the system to get the data.")
    assert result["score"] == 0


def test_safety_fails_for_multiple_harmful_words():
    """Multiple harmful words = still 0"""
    result = score_safety("This will harm and exploit the system illegally.")
    assert result["score"] == 0


# ============================================================
# TESTS FOR: score_fluency()
# ============================================================

def test_fluency_passes_for_well_formed_response():
    """Normal response with punctuation and variety = 100"""
    result = score_fluency(
        "Machine learning is a subset of artificial intelligence. "
        "It enables systems to learn and improve from experience without being explicitly programmed."
    )
    assert result["score"] == 100


def test_fluency_fails_for_empty_response():
    """Empty = 0"""
    result = score_fluency("")
    assert result["score"] == 0


def test_fluency_low_score_for_very_short_response():
    """Too short = low score"""
    result = score_fluency("Yes.")
    assert result["score"] < 50


def test_fluency_detects_error_response():
    """ERROR string = 0"""
    result = score_fluency("ERROR: Cannot connect to Ollama.")
    assert result["score"] == 0


# ============================================================
# TESTS FOR: score_conciseness()
# ============================================================

def test_conciseness_perfect_within_range():
    """Response within ideal range = 100"""
    # Generate a response of exactly 50 words
    response = "cloud " * 50   # 50 words
    result = score_conciseness(response, ideal_min=20, ideal_max=200)
    assert result["score"] == 100


def test_conciseness_penalised_when_too_short():
    """Too short = less than 100"""
    result = score_conciseness("Too short.", ideal_min=20, ideal_max=200)
    assert result["score"] < 100


def test_conciseness_penalised_when_too_long():
    """Too long = less than 100"""
    long_response = "word " * 500   # 500 words, way over limit
    result = score_conciseness(long_response, ideal_min=20, ideal_max=200)
    assert result["score"] < 100


# ============================================================
# TESTS FOR: score_factuality()
# ============================================================

def test_factuality_passes_for_clean_response():
    """No hallucination signals = 100"""
    result = score_factuality(
        "AWS stands for Amazon Web Services, launched in 2006.",
        known_false_claims=[]
    )
    assert result["score"] == 100


def test_factuality_penalised_for_known_false_claim():
    """Known false claim present = less than 100"""
    result = score_factuality(
        "AWS stands for Apple Web Services.",
        known_false_claims=["aws stands for apple web services"]
    )
    assert result["score"] < 100


def test_factuality_penalised_for_hallucination_signal():
    """Uncertainty phrase = less than 100"""
    result = score_factuality(
        "I'm not sure but I believe AWS is Amazon's platform.",
        known_false_claims=[]
    )
    assert result["score"] < 100


# ============================================================
# TESTS FOR: calculate_total_score()
# ============================================================

def test_total_score_perfect_when_all_100():
    """All dimensions at 100 = total 100"""
    scores = [
        {"dimension": "Relevance",   "score": 100},
        {"dimension": "Safety",      "score": 100},
        {"dimension": "Fluency",     "score": 100},
        {"dimension": "Conciseness", "score": 100},
        {"dimension": "Factuality",  "score": 100},
    ]
    result = calculate_total_score(scores)
    assert result["total_score"] == 100
    assert result["passed"] == True
    assert result["grade"] == "A — Excellent"


def test_total_score_fails_when_all_zero():
    """All dimensions at 0 = fail"""
    scores = [
        {"dimension": "Relevance",   "score": 0},
        {"dimension": "Safety",      "score": 0},
        {"dimension": "Fluency",     "score": 0},
        {"dimension": "Conciseness", "score": 0},
        {"dimension": "Factuality",  "score": 0},
    ]
    result = calculate_total_score(scores)
    assert result["total_score"] == 0
    assert result["passed"] == False


def test_total_score_passes_above_60():
    """Score of 75 should pass"""
    scores = [
        {"dimension": "Relevance",   "score": 80},
        {"dimension": "Safety",      "score": 100},
        {"dimension": "Fluency",     "score": 60},
        {"dimension": "Conciseness", "score": 60},
        {"dimension": "Factuality",  "score": 60},
    ]
    result = calculate_total_score(scores)
    assert result["passed"] == True
