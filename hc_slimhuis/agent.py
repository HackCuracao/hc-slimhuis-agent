"""HackCuraçao Slim huis agent.

Stuurt elke 5 minuten een kleine statusmelding (alleen getallen) naar HackCuraçao.
Er staan GEEN open poorten op deze box; de verbinding gaat alleen naar buiten.
Entiteitsnamen, waarden, beelden of adressen worden NOOIT verstuurd: de statussen worden
in het geheugen geteld en daarna weggegooid. Zie ook SECURITY.md.
"""
import json
import os
import time
import urllib.request
from datetime import datetime, timezone

VERSION = "0.1.0"
SUP = "http://supervisor"
TOKEN = os.environ.get("SUPERVISOR_TOKEN", "")
URL = os.environ.get("HC_URL", "")
KEY = os.environ.get("HC_TOKEN", "")


def sup(path):
    req = urllib.request.Request(SUP + path, headers={"Authorization": "Bearer " + TOKEN})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def collect():
    core = sup("/core/info").get("data", {})
    host = sup("/host/info").get("data", {})
    states = sup("/core/api/states")  # alleen in het geheugen geteld, nooit verstuurd
    updates = low = offline = 0
    for s in states:
        eid, st, at = s.get("entity_id", ""), s.get("state"), s.get("attributes", {})
        if eid.startswith("update.") and st == "on":
            updates += 1
        if at.get("device_class") == "battery":
            try:
                if float(st) < 20:
                    low += 1
            except (TypeError, ValueError):
                pass
        if st == "unavailable":
            offline += 1
    age = None
    ok = False
    try:
        backups = sup("/backups").get("data", {}).get("backups", [])
        newest = max((b.get("date") for b in backups if b.get("date")), default=None)
        if newest:
            dt = datetime.fromisoformat(newest.replace("Z", "+00:00"))
            age = max(0, int((datetime.now(timezone.utc) - dt).total_seconds() // 3600))
            ok = True
    except Exception:
        pass
    total = float(host.get("disk_total") or 0)
    used = float(host.get("disk_used") or 0)
    return {
        "v": 1, "agent": VERSION, "ha": str(core.get("version", ""))[:30],
        "uptimeS": int(time.monotonic()),
        "backup": {"ok": ok, "ageH": age},
        "updates": min(updates, 999), "lowBattery": min(low, 999),
        "offline": min(offline, 9999), "devices": min(len(states), 9999),
        "diskPct": int(min(100, used * 100 / total)) if total else 0,
    }


def send(body):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status


def main():
    if not URL or not KEY:
        print("Vul url en token in bij de add-on instellingen.", flush=True)
    while True:
        try:
            if URL and KEY:
                print("heartbeat", send(collect()), flush=True)
        except Exception as e:  # nooit crashen; volgende ronde opnieuw
            print("heartbeat mislukt:", type(e).__name__, flush=True)
        time.sleep(300)


if __name__ == "__main__":
    main()
