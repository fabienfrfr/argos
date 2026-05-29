import requests

BASE_OLLAMA = "http://localhost:11434"
BASE_HERMES = "http://localhost:8080"


def test_ollama_health():
    r = requests.get(f"{BASE_OLLAMA}/api/tags")
    assert r.status_code == 200
    assert "models" in r.json()  # sanity check


def test_hermes_health():
    r = requests.get(BASE_HERMES)
    assert r.status_code == 200