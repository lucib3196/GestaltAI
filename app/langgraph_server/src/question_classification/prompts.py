prompt = """
You are an educational content classifier.

Task:
Analyze the question below and determine whether the retrieved topic documentation
CORRESPONDS to the question.

Question:
{question}

Retrieved Topic Description:
{topic_description}

Instructions:
- Return a binary decision: "YES" or "NO"
- Provide a brief justification (1–2 sentences) explaining your decision
- Base your decision ONLY on conceptual relevance, not wording similarity
- If the topic partially overlaps but does not directly address the core concept,
  return "NO"

Output Format:
Decision: <YES | NO>
Reasoning: <short explanation>
"""
