"""Minimal client for the BLACKBOX AI competition API.

The base URL and your team credentials are given at the event briefing.
Nothing here is secret — it just saves you writing auth boilerplate.

    from src.blackbox import Blackbox

    bb = Blackbox("http://<server>:8000", "BB-017", "your-password")
    print(bb.challenge())     # what your system looks like from outside
    print(bb.quota())         # free - checking never costs a query

    # one row = one query. Batch to save time, not budget.
    out = bb.query([
        {"x1": 0.5, "x2": 0.2, "x3": 0.9},
        {"x1": 0.6, "x2": 0.2, "x3": 0.9},
    ])

    # everything you have ever asked, back as rows. Also free.
    import pandas as pd
    df = pd.DataFrame(bb.export())
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request


class QuotaExhausted(RuntimeError):
    """Your budget for this round is gone. It does not come back."""


class RateLimited(RuntimeError):
    """You are sending too fast. This does NOT cost you quota — back off and retry."""


class Blackbox:
    def __init__(self, base_url: str, team: str, password: str, timeout: int = 30):
        self.base = base_url.rstrip("/")
        self.timeout = timeout
        self.token = self._login(team, password)

    # ---- plumbing -------------------------------------------------------
    def _call(self, method: str, path: str, body: dict | None = None) -> dict:
        req = urllib.request.Request(
            f"{self.base}/api/v1{path}",
            method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Content-Type": "application/json", **getattr(self, "_auth", {})},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            detail = {}
            try:
                detail = json.loads(e.read()).get("error", {})
            except Exception:
                pass
            code = detail.get("code", "")
            msg = detail.get("message", e.reason)
            if code == "QUOTA_EXHAUSTED":
                raise QuotaExhausted(msg) from None
            if code == "RATE_LIMITED":
                raise RateLimited(msg) from None
            raise RuntimeError(f"{code or e.code}: {msg}") from None

    def _login(self, team: str, password: str) -> str:
        self._auth = {}
        tok = self._call("POST", "/auth/login", {"team": team, "password": password})["token"]
        self._auth = {"Authorization": f"Bearer {tok}"}
        return tok

    # ---- the bits you actually use --------------------------------------
    def me(self) -> dict:
        """Team, current round, qualification status."""
        return self._call("GET", "/me")

    def challenge(self) -> dict:
        """Public spec of your assigned challenge: input schema, output schema, budget."""
        return self._call("GET", "/challenge")

    def quota(self) -> dict:
        """limit / used / remaining. Free — does not cost a query."""
        return self._call("GET", "/quota")

    def export(self) -> list[dict]:
        """Every query your team has made, as flat rows. Free.

        In round 4 your earlier queries ARE your training set, so this is how you
        get it back - including anything a teammate ran on another laptop, and
        anything from a session whose browser tab is long gone.

            import pandas as pd
            df = pd.DataFrame(bb.export())
        """
        return self._call("GET", "/queries/export")["queries"]

    def leaderboard(self) -> list[dict]:
        """Published standings. Empty until organisers publish a round."""
        return self._call("GET", "/leaderboard")

    def query(self, rows: list[dict]) -> dict:
        """Send inputs to the black box.

        Each row costs one query. Batching is faster but not cheaper.
        Returns outputs, remaining quota, and a request_id you should record
        in findings.json as evidence.
        """
        if not isinstance(rows, list):
            raise TypeError("query() takes a list of dicts, one per input row")
        return self._call("POST", "/query", {"inputs": rows})
