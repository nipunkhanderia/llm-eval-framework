from llm_caller import call_ollama

# relevence = ["sky", "Blue", "rayleigh", "Scattering", "Nipun"] 

relevence = ["Nipun", "Rhythm", "Payal"] 


def test_relevance():
    response = call_ollama()
    response_lower = response.lower()
    print(response_lower)
    relevance_lower = []
    for word in relevence:
        relevance_lower.append(word.lower())

    # relevance_lower = relevence.lower()
    print (relevance_lower)
    relevence_found = []
    for kw in response_lower.split():
        if kw in relevance_lower:
            relevence_found.append(kw)
            print(kw)
    print(relevence_found)
    if len(relevence_found) > 0:
        print ("Relevency tests passes")
    else:
        print("Relevancy test fails")


test_relevance()