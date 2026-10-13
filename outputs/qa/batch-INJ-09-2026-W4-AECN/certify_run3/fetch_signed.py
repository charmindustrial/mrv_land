"""Download every Certify file whose signed link was captured in signed/<src_id>.json and not yet saved in files/."""
import json, pathlib, subprocess, hashlib, urllib.parse, datetime
H = pathlib.Path(__file__).resolve().parent
man_p = H / "files" / "_download_manifest_run3.json"
man = json.load(open(man_p)) if man_p.exists() else {}
for f in sorted((H / "signed").glob("src_*.json")):
    sid = f.stem
    if sid in man and man[sid].get("http") == "200": continue
    d = json.loads(json.load(open(f)))
    urls = [u for u in d["urls"] if f"/{sid}_" in u]
    if not urls: man[sid] = {"http": "NO_URL", "page": d.get("page")}; continue
    u = urls[0]
    name = urllib.parse.unquote(u.split("?")[0].rsplit("/", 1)[1])
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in name)
    out = H / "files" / safe
    code = subprocess.run(["curl", "-sS", "-m", "120", "-o", str(out), "-w", "%{http_code}", u], capture_output=True, text=True).stdout
    rec = {"file": f"files/{safe}", "http": code, "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    if code == "200":
        rec["bytes"] = out.stat().st_size; rec["sha256"] = hashlib.sha256(out.read_bytes()).hexdigest()
        r2 = list((H.parent / "run2_2026-10-07_superseded" / "certify_run2" / "files").glob(f"{sid}_*"))
        rec["same_as_run2"] = bool(r2) and hashlib.sha256(r2[0].read_bytes()).hexdigest() == rec["sha256"]
    man[sid] = rec
json.dump(man, open(man_p, "w"), indent=1)
ok = [k for k, v in man.items() if v.get("http") == "200"]
print("downloaded:", len(ok), "| not ok:", {k: v.get("http") for k, v in man.items() if v.get("http") != "200"},
      "| differ from run 2:", [k for k in ok if not man[k].get("same_as_run2")])
