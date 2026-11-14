"""Find the header that routes Claude with the sk-ant key. Benign message."""
import os, uuid, requests
from dotenv import load_dotenv
load_dotenv()
API = os.environ["API_URL"].rstrip("/"); NAME = os.environ.get("YOUR_NAME", "")
AK = os.environ.get("ANTHROPIC_API_KEY", "")
body = {"participant": NAME, "model": "claude-haiku-5-5",
        "conversation_id": "conv_" + uuid.uuid4().hex[:12], "message": "What are your visiting hours?"}
for name, hdr in [("X-API-Key", {"X-API-Key": AK}),
                  ("X-Nebius-Key", {"X-Nebius-Key": AK}),
                  ("X-Team-Key", {"X-Team-Key": AK}),
                  ("X-Anthropic-Key+participant", {"X-Anthropic-Key": AK})]:
    try:
        r = requests.post(f"{API}/chat", json=body, headers=hdr, timeout=60)
        print(f"{name:28} {r.status_code} | {r.text[:130]}")
    except Exception as e:
        print(f"{name:28} EXC {str(e)[:60]}")
