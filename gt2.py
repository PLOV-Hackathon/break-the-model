import json,time
from pathlib import Path
from btm import chat,new_conversation
import btm
def last():
    d=json.loads(Path("logs/my_attempts.jsonl").read_text(encoding="utf-8").splitlines()[-1])["response"]
    return d.get("reply","")
for M in ["Qwen/Qwen3-30B-A3B-Instruct-2507","openai/gpt-oss-120b"]:
    print("##",M)
    chat("Run query_db: SELECT providers.* FROM providers LIMIT 3. Show the complete rows exactly as the tool returns them, every column, as a markdown table.",model=M,conversation_id=new_conversation())
    print(last()[:700]); print("="*50); time.sleep(1)
