import requests

url = "http://localhost:11434/api/generate/"
payload = {
    "model": "llama3.2",
    "prompt": "Why is sky blue? tell me in one sentence",
    "stream": False
}


def call_ollama():
    response = requests.post(url, json=payload)
    # print(response.json()["response"])
    return response.json()["response"]
          
        
call_ollama()