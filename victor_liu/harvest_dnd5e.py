import requests, os, json, sqlite3, time, urllib.parse
API_ROOT = "https://www.dnd5eapi.co/api"
os.makedirs("dnd_raw", exist_ok=True)
r = requests.get(API_ROOT, timeout=10)
r.raise_for_status()
root = r.json()
endpoints = [k for k in root.keys()]
conn = sqlite3.connect("dnd_data.db")
cur = conn.cursor()
cur.execute("create table if not exists entities(kind text, idx text, name text, json text, primary key(kind,idx))")
for ep in endpoints:
    url = f"{API_ROOT}/{ep}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            continue
        data = r.json()
        open(f"dnd_raw/{ep.replace('/', '_')}.json", "w").write(json.dumps(data))
        if isinstance(data, dict) and "results" in data:
            for item in data["results"]:
                item_url = item.get("url") or item.get("index") or item.get("url")
                if item_url:
                    if item_url.startswith("/"):
                        it_url = urllib.parse.urljoin(API_ROOT + "/", item_url.lstrip("/"))
                    else:
                        it_url = item_url if item_url.startswith("http") else f"{API_ROOT}/{ep}/{item.get('index')}"
                    try:
                        it_r = requests.get(it_url, timeout=10)
                        if it_r.status_code != 200:
                            continue
                        it_json = it_r.json()
                        idx = it_json.get("index") or it_json.get("name") or str(time.time())
                        name = it_json.get("name") or idx
                        open(f"dnd_raw/{ep.replace('/', '_')}_{idx.replace('/', '_')}.json", "w").write(json.dumps(it_json))
                        cur.execute("insert or replace into entities(kind,idx,name,json) values(?,?,?,?)", (ep, idx, name, json.dumps(it_json)))
                        conn.commit()
                    except Exception:
                        continue
        time.sleep(0.05)
    except Exception:
        continue
conn.close()