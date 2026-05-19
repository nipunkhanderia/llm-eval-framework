from llm_caller import call_ollama

relevance = ["Sky", "Rayleigh", "Scattering", "Wavelength", "nipun"]

def test_relevance():
    response = call_ollama()
    # print(response)
    response_lower = response.lower()
    print(response_lower)
    rel_lower = []
    for rel in relevance:
        rel = rel.lower()
        rel_lower.append(rel)
    
    print(rel_lower)


    # print(relevance.lower())
    found = []
    for kw in rel_lower:
        if kw in response_lower:
            found.append(kw)
    print (found)
    if (len(found)) > 0:
        print("kw found")
    else:
        print("kw failed")

test_relevance()
