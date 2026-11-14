"""Probe whether Entropy's server routes Claude model ids with the Anthropic key.
Benign message only (routing test, not an attack). Tries model-id x header combos."""
import os, uuid, requests
from dotenv import load_dotenv
load_dotenv()
API = os.environ["API_URL"].rstrip("/")
NAME = os.environ.get("YOUR_NAME", "")
AK = os.environ.get("ANTHROPIC_API_KEY", "")
NK = [l.split("=", 1)[1].strip() for l in open(".env") if l.startswith("NEBIUS_API_KEY=")]
NK = NK[0] if NK else ""
print("ANTHROPIC_API_KEY present:", bool(AK))

models = ["claude-haiku-5-5", "claude-sonnet-5-5", "anthropic/claude-haiku-5-5",
          "anthropic/claude-sonnet-5-5", "claude-5.5-haiku", "claude-haiku-5.5"]
def headers(variant):
    return {
        "xanthropic": {"X-Anthropic-Key": AK},
        "bearer":     {"Authorization": f"Bearer {AK}"},
        "xapikey":    {"X-API-Key": AK},
        "nebius+anth":{"X-Nebius-Key": NK, "X-Anthropic-Key": AK},
    }[variant]

msg = "What are your visiting hours?"
seen = set()
for m in models:
    for hv in ["xanthropic", "bearer", "xapikey", "nebius+anth"]:
        body = {"participant": NAME, "model": m,
                "conversation_id": "conv_" + uuid.uuid4().hex[:12], "message": msg}
        try:
            r = requests.post(f"{API}/chat", json=body, headers=headers(hv), timeout=60)
            snip = (r.text or "")[:120].replace("\n", " ")
        except Exception as e:
            snip = f"EXC {str(e)[:50]}"
        key = (m, hv, r.status_code if 'r' in dir() else '?')
        print(f"{m:28} {hv:12} -> {getattr(r,'status_code','?')} | {snip!r}")
