def ask_rag(question: str):
    """
    Fake RAG pipeline for demo purposes.
    Replace this with your actual LangChain/LlamaIndex pipeline.
    """

    knowledge_base = {
        "What is pytest?":
            "pytest is a Python testing framework used for unit and integration testing.",

        "What is RAG?":
            "RAG stands for Retrieval-Augmented Generation."
    }

    answer = knowledge_base.get(
        question,
        "I do not know."
    )

    retrieved_context = [
        answer
    ]

    return {
        "question": question,
        "answer": answer,
        "contexts": retrieved_context
    }
