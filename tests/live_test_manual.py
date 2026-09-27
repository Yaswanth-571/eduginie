"""Quick live test of all 5 EduGenie endpoints."""
import urllib.request
import json

BASE = "http://127.0.0.1:8000"


def post(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{BASE}{path}", data=data,
        headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.loads(r.read())
            print(f"[OK]   {path}")
            return body
    except urllib.error.HTTPError as e:
        print(f"[FAIL] {path} -> {e.code}: {e.read().decode()[:300]}")
        return None


# GET /
req = urllib.request.Request(f"{BASE}/")
with urllib.request.urlopen(req) as r:
    print(f"[OK]   GET / -> {r.status}")

# Q&A
r = post("/qa", {"question": "What is DNA?"})
if r:
    print("       answer:", r["answer"][:90])

# Explain
r = post("/explain", {"topic": "Gravity"})
if r:
    print("       explanation:", r["explanation"][:90])

# Summarize
r = post("/summarize", {
    "text": (
        "Photosynthesis is the process used by plants to convert light into energy. "
        "It occurs in chloroplasts and produces glucose and oxygen."
    )
})
if r:
    print("       summary:", r["summary"][:90])

# Quiz
r = post("/quiz", {
    "text": (
        "Photosynthesis is the process used by plants to convert light into energy. "
        "It occurs in chloroplasts using chlorophyll pigments. "
        "The products are glucose and oxygen. "
        "Plants absorb carbon dioxide and water for this process."
    )
})
if r:
    num_q = len(r["questions"])
    print(f"       quiz questions: {num_q}")
    for i, q in enumerate(r["questions"]):
        opts = len(q["options"])
        ca_in = q["correct_answer"] in q["options"]
        print(f"       Q{i+1}: opts={opts}, ca_in_opts={ca_in}, q={q['question'][:55]}")

# Learn
r = post("/learn/recommendations", {"topic": "Python", "level": "beginner"})
if r:
    print("       recommendations:", r["recommendations"][:90])
