Feature: RAG evaluation

  Scenario: Evaluate RAG response quality
    Given a user asks "What is pytest?"
    When the RAG system generates a response
    Then the response should pass DeepEval metrics
    And the response should pass Ragas metrics
