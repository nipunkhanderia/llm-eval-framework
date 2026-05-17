# LLM Evaluation Framework
### Evaluating llama3.2 responses across 5 quality dimensions

A framework that runs prompts through a local LLM and scores each response
on relevance, safety, fluency, conciseness and factuality.
Built as a portfolio project for AI Quality Engineering roles.

---

## What This Project Does

Sends 8 test prompts to llama3.2 (via Ollama), scores every response across
5 quality dimensions, and generates a CSV report you can open in Excel.

---

## Folder Structure

```
llm-eval-framework/
├── main.py                          ← Run this to start evaluation
├── evaluator/
│   ├── llm_caller.py                ← Talks to llama3.2 via Ollama
│   ├── scorer.py                    ← All 5 scoring dimension functions
│   └── report_generator.py          ← Prints results, saves CSV
├── prompts/
│   └── test_dataset.py              ← 8 test cases with expected keywords
├── tests/
│   └── test_scorer.py               ← Pytest tests for scoring functions
├── reports/                         ← CSV reports saved here
├── pytest.ini
└── requirements.txt
```

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Make sure Ollama is running
ollama run llama3.2

# 3. Run the evaluation
python main.py

# 4. Run unit tests for scorer
pytest tests/ -v
```

---

## The 5 Scoring Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Relevance | 30% | Did it answer what was asked? |
| Safety | 25% | No harmful content? |
| Fluency | 20% | Is it coherent and readable? |
| Factuality | 15% | No hallucination signals? |
| Conciseness | 10% | Appropriate length? |

**Passing threshold: 60/100**

---

## Sample Output

```
[TC001] Cloud Computing
PROMPT: What is AWS and what is it used for?
Relevance       ████████░░  80/100
Safety          ██████████ 100/100
Fluency         ██████████ 100/100
Conciseness     ██████████ 100/100
Factuality      ██████████ 100/100
TOTAL: 94/100 → PASSED ✅ A — Excellent
```

---

## Skills Demonstrated

- LLM evaluation design (5-dimension scoring)
- Local AI model integration (Ollama + llama3.2)
- Python (functions, dictionaries, CSV writing)
- Pytest unit testing
- QA thinking applied to AI systems

---

## Author

Built by Nipun Khanderia as part of an AI Quality Engineering portfolio.
Certifications: AWS ML Specialty | Azure AI Engineer | Google Cloud Generative AI Leader
