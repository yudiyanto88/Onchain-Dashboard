import requests, time, sys, json
key = [l.split('=',1)[1].strip() for l in open('.env', encoding='utf-8-sig') if l.startswith('DUNE_API_KEY=')][0]
H = {'X-Dune-API-Key': key}
def q(sql, perf='medium'):
    r = requests.post('https://api.dune.com/api/v1/sql/execute', headers=H, json={'sql': sql, 'performance': perf}, timeout=60)
    if not r.ok: return {'error': r.status_code, 'text': r.text[:400]}
    eid = r.json()['execution_id']
    while True:
        s = requests.get(f'https://api.dune.com/api/v1/execution/{eid}/results', headers=H, timeout=120).json()
        if s.get('is_execution_finished'):
            return s
        time.sleep(3)
if __name__ == '__main__':
    s = q(open(sys.argv[1], encoding='utf-8').read())
    if 'result' in s:
        rows = s['result']['rows']; print('baris', len(rows), '| state', s.get('state'))
        for r in rows[:int(sys.argv[2]) if len(sys.argv) > 2 else 60]: print(r)
    else:
        print(json.dumps(s)[:1500])
