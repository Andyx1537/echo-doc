"""Standalone local inference evidence capture; no Echo integration or training."""
import datetime
import hashlib
import json
from pathlib import Path
import time
import urllib.request

BASE = Path(__file__).resolve().parent
URL = 'http://127.0.0.1:11434'

def api(path, payload=None):
    body = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(URL + path, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as res:
        return json.load(res)

run_id = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
out = Path('/Users/andy/Models/echo-local/runs') / run_id
out.mkdir(parents=True, exist_ok=False)
prompt = (BASE / 'prompts/material-pack-v1.txt').read_text()
cases = json.loads((BASE / 'fixtures/smoke.json').read_text())
meta = {'run_id': run_id, 'runtime': api('/api/version'), 'models': api('/api/tags'),
        'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
        'fixtures_sha256': hashlib.sha256((BASE / 'fixtures/smoke.json').read_bytes()).hexdigest(),
        'note': 'Sequential first-load then warm requests; structural check only, semantic review required.'}
(out / 'manifest.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2))
for case in cases:
    payload = {'model': 'qwen3:14b', 'stream': False, 'think': False, 'format': 'json',
               'keep_alive': '5m', 'options': {'num_ctx': 4096, 'temperature': 0, 'num_predict': 1024},
               'messages': [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': json.dumps(case, ensure_ascii=False)}]}
    record = {'case': case, 'request': payload}
    start = time.monotonic()
    try:
        response = api('/api/chat', payload)
        record['response'] = response
        parsed = json.loads(response['message']['content'])
        record['required_keys_present'] = isinstance(parsed, dict) and all(k in parsed for k in ['subject','scenes','facts','creative_suggestions','next_question'])
        record['truncated'] = response.get('done_reason') == 'length'
    except Exception as exc:
        record['error'] = str(exc)
    record['elapsed_seconds'] = time.monotonic() - start
    (out / (case['id'] + '.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2))
    print(json.dumps({'case':case['id'], 'seconds':record['elapsed_seconds'], 'keys':record.get('required_keys_present'), 'error':record.get('error')}, ensure_ascii=False), flush=True)
print(str(out), flush=True)
