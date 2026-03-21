
import os
import re

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


ROLE_KEYWORDS = {
    "Backend Developer": ["api", "server", "database", "authentication", "middleware", "scalable", "sql", "nosql"],
    "Frontend Developer": ["ui", "responsive", "component", "state", "dom", "browser", "performance", "accessibility"],
    "Full Stack Developer": ["frontend", "backend", "api", "database", "authentication", "deploy", "scalable"],
    "Data Scientist": ["data", "model", "feature", "missing", "overfitting", "classification", "regression", "metric"],
    "AI & ML Developer": ["model", "train", "validate", "loss", "hyperparameter", "embedding", "deploy", "overfitting"],
    "Tester": ["test", "bug", "regression", "smoke", "qa", "automation", "manual", "scenario"],
    "Designer": ["ux", "ui", "accessibility", "consistency", "typography", "color", "feedback", "user-friendly"],
    "Python Developer": ["python", "list", "tuple", "module", "comprehension", "exception", "oop", "object-oriented"],
    "Java Developer": ["java", "jvm", "jre", "jdk", "interface", "abstract", "exception", "thread", "collection"],
    "UI Developer": ["ui", "ux", "design", "accessibility", "hierarchy", "interaction", "consistent", "dashboard"],
}

GENERAL_GOOD_WORDS = [
    "example", "because", "first", "then", "next", "result", "improve", "handle",
    "build", "manage", "develop", "design", "learn", "practice", "team"
]


def _normalize(text):
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def evaluate_answer(question, answer, role=None):
    q = _normalize(question)
    a = _normalize(answer)

    score = 0

    # basic quality
    if len(a.split()) >= 8:
        score += 2
    if len(a.split()) >= 20:
        score += 2

    # question awareness
    q_keywords = [w for w in re.findall(r"[a-z0-9&]+", q) if len(w) > 3]
    matched = sum(1 for w in q_keywords if w in a)
    if matched > 0:
        score += 2

    # role relevance
    keywords = ROLE_KEYWORDS.get(role, [])
    relevance = sum(1 for kw in keywords if kw in a)
    score += min(relevance * 1, 4)

    # general answer quality
    general = sum(1 for kw in GENERAL_GOOD_WORDS if kw in a)
    if general >= 2:
        score += 1

    return min(score, 10)


def generate_feedback(payload):
    role = payload.get("role", "Unknown")
    answers = payload.get("answers", [])
    scores = payload.get("scores", [])
    total_score = payload.get("total_score", 0)

    if OpenAI is not None and os.getenv("OPENAI_API_KEY"):
        try:
            client = OpenAI()
            prompt = f"""
You are an interview coach.
Role: {role}
Scores: {scores}
Total score: {total_score}
Answers: {answers}

Return a short professional feedback with:
- Strengths
- Weaknesses
- Improvements
Keep it concise and clear.
"""
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content.strip()
        except Exception:
            pass

    # local fallback
    if total_score >= 8:
        level = "Excellent work. Your answers were clear and relevant."
    elif total_score >= 5:
        level = "Good attempt. Add more role-specific details and examples."
    else:
        level = "Needs improvement. Try to explain concepts with more clarity and confidence."

    return (
        f"Strengths: You answered with some structure and showed basic understanding.\n"
        f"Weaknesses: Some answers need more technical detail and role relevance.\n"
        f"Improvements: Practice using examples, keywords from the role, and a clearer explanation style.\n"
        f"Overall: {level}"
    )
