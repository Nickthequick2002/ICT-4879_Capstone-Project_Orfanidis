import os
from openai import OpenAI


SYSTEM_PROMPT = """
You are FitTrack's AI assistant.
You help users with fitness, workouts, and nutrition.

Rules:
- Keep answers SHORT (2–3 sentences max).
- Be clear, practical, and friendly.
- Use bullet points only if helpful.
- Do NOT give medical advice.
- Avoid unnecessary explanations.
"""

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=api_key)

def ai_reply(user_message):
    client = get_client()  # ✅ created ONLY when needed

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        max_tokens=120
    )

    return response.choices[0].message.content.strip()
