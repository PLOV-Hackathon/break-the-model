"""Check Claude access with whatever key is in .env (API_KEY or ANTHROPIC_API_KEY), X-API-Key header."""
import os, re, uuid, requests
from dotenv import load_dotenv
load_dotenv()
API = os.environ["API_URL"].rstrip("/"); NAME = os.environ.get("YOUR_NAME", "")
# prefer API_KEY (new format); fall back to ANTHROPIC_API_KEY; strip whitespace
key = ""
for ln in open(".env", encoding="utf-8"):
    if ln.startswith("API_KEY=") or ln.startswith("ANTHROPIC_API_KEY="):
        v = re.sub(r"\s+", "", ln.split("=", 1)[1])
        if v.startswith("sk-ant-"):
            key = v; break
print("anthropic key found:", bool(key), "len", len(key))
for m in ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]:
    body = {"participant": NAME, "model": m,
            "conversation_id": "conv_" + uuid.uuid4().hex[:12], "message": "What are your visiting hours?"}
    r = requests.post(f"{API}/chat", json=body, headers={"X-API-Key": key}, timeout=90)
    print(f"{m:20} {r.status_code} | {r.text[:110]}")
