"""Route Claude via X-API-Key with the sk-ant key, whitespace stripped. Benign test."""
import os, re, uuid, requests
from dotenv import load_dotenv
load_dotenv()
API = os.environ["API_URL"].rstrip("/"); NAME = os.environ.get("YOUR_NAME", "")
raw = os.environ.get("ANTHROPIC_API_KEY", "")
key = re.sub(r"\s+", "", raw)   # paste had embedded spaces
print("raw_len", len(raw), "clean_len", len(key), "prefix_ok", key.startswith("sk-ant-"))
body = {"participant": NAME, "model": "claude-haiku-5-5",
        "conversation_id": "conv_" + uuid.uuid4().hex[:12], "message": "What are your visiting hours?"}
r = requests.post(f"{API}/chat", json=body, headers={"X-API-Key": key}, timeout=90)
print(r.status_code, "|", r.text[:160])
