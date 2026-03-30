from openai import OpenAI

client = OpenAI()

def generate_feedback(answers):

    prompt=f"""
    Provide interview feedback.

    Answers:
    {answers}

    Give:
    strengths
    weaknesses
    improvements
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content