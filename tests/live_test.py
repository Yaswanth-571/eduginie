"""
Live endpoint test runner against running Uvicorn server (http://127.0.0.1:8000).
Tests all 5 features:
1. POST /qa
2. POST /explain
3. POST /quiz (including structured JSON validation)
4. POST /summarize
5. POST /learn/recommendations
"""
import sys
import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    client = httpx.Client(base_url=BASE_URL, timeout=60.0)

    # 1. Health / Home check
    print("Testing GET / ...")
    r = client.get("/")
    assert r.status_code == 200, f"GET / failed with {r.status_code}"
    print("  GET / -> OK (200)")

    # 2. Q&A
    print("Testing POST /qa ...")
    r = client.post("/qa", json={"question": "What is the primary function of mitochondria?"})
    assert r.status_code == 200, f"POST /qa failed: {r.status_code} - {r.text}"
    qa_data = r.json()
    assert "answer" in qa_data and len(qa_data["answer"]) > 10
    print(f"  POST /qa -> OK (200) | Preview: {qa_data['answer'][:60]}...")

    # 3. Concept Explanation
    print("Testing POST /explain ...")
    r = client.post("/explain", json={"topic": "Binary Search"})
    assert r.status_code == 200, f"POST /explain failed: {r.status_code} - {r.text}"
    explain_data = r.json()
    assert "explanation" in explain_data and len(explain_data["explanation"]) > 10
    print(f"  POST /explain -> OK (200) | Preview: {explain_data['explanation'][:60]}...")

    # 4. Quiz Generation (Structured JSON validation)
    print("Testing POST /quiz ...")
    sample_text = (
        "Photosynthesis is the biochemical process by which green plants, algae, and some bacteria "
        "convert light energy into chemical energy stored in glucose. The process takes place in the "
        "chloroplasts, primarily using chlorophyll pigments to absorb sunlight, carbon dioxide from the air, "
        "and water from the soil, producing oxygen as a byproduct."
    )
    r = client.post("/quiz", json={"text": sample_text})
    assert r.status_code == 200, f"POST /quiz failed: {r.status_code} - {r.text}"
    quiz_data = r.json()
    assert "questions" in quiz_data
    questions = quiz_data["questions"]
    assert len(questions) == 3, f"Expected 3 questions, got {len(questions)}"
    for idx, q in enumerate(questions, 1):
        assert "question" in q and q["question"]
        assert "options" in q and len(q["options"]) == 4, f"Q{idx} options count != 4"
        assert "correct_answer" in q and q["correct_answer"] in q["options"], f"Q{idx} correct_answer not in options"
    print("  POST /quiz -> OK (200) | Successfully validated 3 questions, each with 4 options and valid answer key.")

    # 5. Summarization
    print("Testing POST /summarize ...")
    r = client.post("/summarize", json={"text": sample_text})
    assert r.status_code == 200, f"POST /summarize failed: {r.status_code} - {r.text}"
    summary_data = r.json()
    assert "summary" in summary_data and len(summary_data["summary"]) > 10
    print(f"  POST /summarize -> OK (200) | Preview: {summary_data['summary'][:60]}...")

    # 6. Learning Path
    print("Testing POST /learn/recommendations ...")
    r = client.post("/learn/recommendations", json={"topic": "Python Web Development", "level": "beginner"})
    assert r.status_code == 200, f"POST /learn/recommendations failed: {r.status_code} - {r.text}"
    learn_data = r.json()
    assert "recommendations" in learn_data and len(learn_data["recommendations"]) > 10
    print(f"  POST /learn/recommendations -> OK (200) | Preview: {learn_data['recommendations'][:60]}...")

    print("\nALL 5 ENDPOINTS TESTED SUCCESSFULLY AGAINST LIVE GEMINI API!")

if __name__ == "__main__":
    test_endpoints()
