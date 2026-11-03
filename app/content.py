import os, json

DEMO = {
    "title": "Why do your fingers wrinkle in water?",
    "narration": (
        "Why do your fingers wrinkle after a long bath? It is not simply water "
        "soaking into your skin. Your nervous system causes blood vessels in your "
        "fingertips to narrow, pulling the skin into ridges. Scientists think those "
        "ridges may help you grip wet objects, a little like tire treads moving water. "
        "Here is the strange part: when certain nerves are damaged, the wrinkles may "
        "not appear normally. So those tiny creases are not random. They are a response "
        "controlled by your body."
    ),
    "scenes": [
        "A cartoon hand dips into a clear bath",
        "Close-up of fingertips forming wrinkles",
        "A colorful cutaway shows tiny blood vessels narrowing",
        "A hand grips a slippery glass",
        "A dramatic close-up of wrinkled fingertips"
    ]
}

def generate_story():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return DEMO
    from openai import OpenAI
    client = OpenAI(api_key=key)
    prompt = """Create an original YouTube Shorts script, 105-130 words.
Choose a surprising science fact, human-body mystery, what-if scenario, or
well-documented unbelievable story. Start with a gripping one-sentence hook,
escalate with clear explanations, and end with a memorable payoff. Keep claims
accurate; do not invent facts, give medical advice, imitate a specific creator,
or use copyrighted characters. Return JSON only with title, narration, scenes.
Scenes must be exactly five concise visual descriptions."""
    result = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    data = json.loads(result.choices[0].message.content)
    if not all(k in data for k in ("title", "narration", "scenes")) or len(data["scenes"]) != 5:
        raise ValueError("AI returned an invalid story structure")
    return data
