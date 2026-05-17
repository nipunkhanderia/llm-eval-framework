# ============================================================
# evaluator/llm_caller.py
# ============================================================
# PURPOSE:
#   Same job as api_caller.py in Project 1.
#   ONE job only — talk to llama3.2 via Ollama and return response.
#
# WHY SAME PATTERN:
#   You already understand this pattern from Project 1.
#   Consistency across projects = good engineering habit.
#   If Ollama changes tomorrow, we only fix THIS file.
#
# PRE-REQUISITE:
#   Ollama must be running with llama3.2 pulled.
#   Terminal: ollama run llama3.2
# ============================================================

import requests   # For HTTP calls to Ollama
import time       # For measuring how long responses take

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


def call_llm(prompt: str, max_tokens: int = 300) -> dict:
    """
    Sends a prompt to llama3.2 and returns BOTH the response
    AND metadata about the call (time taken, success etc.)

    WHY RETURN A DICT INSTEAD OF JUST TEXT:
        In Project 1 we only needed the text.
        In an evaluation framework we also need:
        - How long did it take? (latency)
        - Did it succeed or error?
        - What was the exact prompt sent?
        All of this goes into our evaluation scores.

    Parameters:
        prompt     : The question or instruction to send
        max_tokens : Maximum response length (default 300)

    Returns:
        A dictionary with:
            "success"  : True or False
            "prompt"   : The original prompt we sent
            "response" : The text response from the model
            "latency"  : How many seconds the call took
            "error"    : Error message if success is False
    """

    # Record start time so we can measure how long it takes
    start_time = time.time()

    request_body = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": max_tokens
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=request_body, timeout=120)
        latency = round(time.time() - start_time, 2)  # seconds, 2 decimal places

        if response.status_code != 200:
            return {
                "success": False,
                "prompt": prompt,
                "response": "",
                "latency": latency,
                "error": f"Ollama returned status {response.status_code}"
            }

        response_text = response.json()["response"].strip()

        return {
            "success": True,
            "prompt": prompt,
            "response": response_text,
            "latency": latency,
            "error": None
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "prompt": prompt,
            "response": "",
            "latency": round(time.time() - start_time, 2),
            "error": "Cannot connect to Ollama. Run: ollama run llama3.2"
        }

    except Exception as e:
        return {
            "success": False,
            "prompt": prompt,
            "response": "",
            "latency": round(time.time() - start_time, 2),
            "error": str(e)
        }


# ============================================================
# QUICK TEST
# python evaluator/llm_caller.py
# ============================================================

if __name__ == "__main__":
    print("Testing Ollama connection...")
    result = call_llm("What is software testing? Answer in one sentence.")

    if result["success"]:
        print(f"SUCCESS in {result['latency']}s")
        print(f"Response: {result['response']}")
    else:
        print(f"FAILED: {result['error']}")
