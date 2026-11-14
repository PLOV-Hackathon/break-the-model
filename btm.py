"""Break the Model — tiny client. Every call is also saved to logs/my_attempts.jsonl."""
import json, os, time, uuid
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()
API = os.environ["API_URL"].rstrip("/")
NAME = os.environ.get("YOUR_NAME", "")
def _load_keys():
    """All NEBIUS_API_KEY values from .env (the user pasted several on identical lines; os.environ
    would keep only the last, so read the file directly). Falls back to the environment."""
    keys, env = [], Path(__file__).parent / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("NEBIUS_API_KEY="):
                v = line.split("=", 1)[1].strip()
                if v and v != "paste-your-nebius-key-here" and v not in keys:
                    keys.append(v)
    if not keys and os.environ.get("NEBIUS_API_KEY"):
        keys.append(os.environ["NEBIUS_API_KEY"])
    return keys

KEYS = _load_keys()
if not KEYS:
    raise RuntimeError("No NEBIUS_API_KEY in .env")
KEY = KEYS[0]            # back-compat for other scripts
_KI = 0                  # current key index, rotated on rate-limit


def _scan_keys():
    """Anthropic (sk-ant-) and Groq (gsk_) keys from .env, any field name."""
    anth = groq = ""
    env = Path(__file__).parent / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line:
                v = line.split("=", 1)[1].strip()
                if v.startswith("sk-ant-") and not anth:
                    anth = v
                elif v.startswith("gsk_") and not groq:
                    groq = v
    return anth, groq

ANTH, GROQ = _scan_keys()
LOG = Path(__file__).parent / "logs" / "my_attempts.jsonl"
LOG.parent.mkdir(exist_ok=True)
LAST_TURN_ID = None


def list_models():
    return [m["id"] for m in requests.get(f"{API}/models", timeout=30).json()["models"]]


def new_conversation():
    return "conv_" + uuid.uuid4().hex[:12]


def chat(message, model, conversation_id=None):
    """Send one message. Reuse the same conversation_id to keep talking in one conversation."""
    body = {"participant": NAME, "model": model,
            "conversation_id": conversation_id or new_conversation(), "message": message}
    global _KI
    if model.startswith("claude"):                   # Anthropic via X-API-Key
        keyset, hdr = [ANTH], "X-API-Key"
    elif model.startswith("groq/"):                   # Groq via X-API-Key (gsk_ key)
        keyset, hdr = ([GROQ] if GROQ else KEYS), "X-API-Key"
    else:                                             # Nebius via X-Nebius-Key (rotating)
        keyset, hdr = KEYS, "X-Nebius-Key"
    idx = _KI % len(keyset)
    for _ in range(len(keyset)):                      # rotate to the next key on rate-limit / quota
        r = requests.post(f"{API}/chat", json=body, headers={hdr: keyset[idx]}, timeout=300)
        try:
            data = r.json()
        except Exception:  # noqa: BLE001
            data = {"error": r.text[:200]}
        if r.status_code == 429 or "rate limit" in str(data).lower() or "quota" in str(data).lower():
            idx = (idx + 1) % len(keyset)
            if keyset is KEYS:
                _KI = idx
            time.sleep(1)
            continue
        break
    with LOG.open("a") as f:
        f.write(json.dumps({"ts": time.strftime("%H:%M:%S"), "request": body, "response": data}) + "\n")
    if r.status_code != 200:
        raise RuntimeError(f"Error {r.status_code}: {data}")
    for tc in data.get("tool_calls") or []:
        print(f"  [Riley used tool: {tc['name']}]")
    global LAST_TURN_ID
    LAST_TURN_ID = data["turn_id"]
    return data["reply"]
