import os
import re
import urllib.request
from urllib.error import HTTPError
from urllib.parse import urlencode


def send_whatsapp(number, text, api_key=""):
    """Returns (ok: bool, info: str). Uses CallMeBot (free)."""
    key = (api_key or os.environ.get("CALLMEBOT_API_KEY", "")).strip()
    number = re.sub(r"\D", "", number or "")
    if not key:
        return False, "API key is empty (Contact Section > Email & WhatsApp)"
    if not number:
        return False, "WhatsApp number is empty"

    url = "https://api.callmebot.com/whatsapp.php?" + urlencode({"phone": "+" + number, "text": text, "apikey": key})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read().decode("utf-8", "ignore")
            code = r.status
    except HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        code = e.code
    except Exception as e:
        return False, "Request failed: " + repr(e)[:150]

    plain = re.sub(r"<[^>]+>", " ", body)
    plain = " ".join(plain.split())[:160]
    ok = code == 200 and "queued" in plain.lower()
    return ok, f"HTTP {code}: {plain}"