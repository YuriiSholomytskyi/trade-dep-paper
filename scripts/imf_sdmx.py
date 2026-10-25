"""Shared helper for pulling data from the IMF SDMX 3.0 API.

The IMF retired its legacy data portal in Nov 2025; everything now lives at
https://api.imf.org/external/sdmx/3.0 . This module wraps the structure and
data endpoints we use across the project.

Notes learned the hard way:
- Reporter wildcard in a data key must be '*' (an empty string returns nothing).
- Multi-code dims are '+'-joined, e.g. CHN+G001 or XG_FOB_USD+MG_CIF_USD.
- IMF.org *publication* pages 403 to bots, but the api.imf.org endpoints do NOT.
"""
import io
import ssl
import time
import urllib.request

import pandas as pd

BASE = "https://api.imf.org/external/sdmx/3.0"
_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE
_HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.sdmx.data+csv"}


def _open(url, timeout=600):
    req = urllib.request.Request(url, headers=_HEADERS)
    return urllib.request.urlopen(req, context=_CTX, timeout=timeout)


def fetch_data(agency, dataflow, key, start=None, version="+", timeout=600):
    """Return a tidy DataFrame for an SDMX data query (sdmx-csv format)."""
    url = f"{BASE}/data/dataflow/{agency}/{dataflow}/{version}/{key}?format=sdmx-csv"
    if start:
        url += f"&startPeriod={start}"
    t = time.time()
    raw = _open(url, timeout).read().decode("utf-8", "replace")
    df = pd.read_csv(io.StringIO(raw))
    print(f"[fetch_data] {dataflow} {key} -> {len(df)} rows, "
          f"{round(len(raw)/1e6, 1)} MB, {round(time.time()-t, 1)}s")
    return df


def fetch_structure_json(path, timeout=180):
    """Return parsed JSON for a structure endpoint (format=sdmx-json)."""
    import json
    sep = "&" if "?" in path else "?"
    url = f"{BASE}/structure/{path}{sep}format=sdmx-json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, context=_CTX, timeout=timeout))


def to_period_dt(series, freq="M"):
    """Convert IMF TIME_PERIOD strings ('2026-M02' / '2026') to datetime."""
    s = series.astype(str)
    if freq == "M":
        return pd.to_datetime(s.str.replace("-M", "-", regex=False),
                              format="%Y-%m", errors="coerce")
    return pd.to_datetime(s, format="%Y", errors="coerce")
