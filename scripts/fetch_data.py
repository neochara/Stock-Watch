from __future__ import annotations

import os
import time
import random
import argparse
from typing import Dict, List, Optional

import pandas as pd
import yfinance as yf

from constants import STOCK_DATA_DICT, START_DATE, TODAY


class RetryableDownloadError(Exception):
    pass


def data_dir() -> str:
    root = os.path.dirname(os.path.abspath(__file__))
    d = os.path.join(root, "data")
    os.makedirs(d, exist_ok=True)
    return d


def tickers() -> List[str]:
    out = []
    for _, sym in STOCK_DATA_DICT.items():
        s = str(sym).strip().upper()
        if s and s not in out:
            out.append(s)
    return out


def csv_path(ticker: str) -> str:
    return os.path.join(data_dir(), f"{ticker.lower()}_stock.csv")


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return df

    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.index.name = "Date"
    return df


def is_valid_price_df(df: pd.DataFrame) -> bool:
    """
    Strong validation: reject "empty-ish" frames (0 rows or all-NaN prices),
    which commonly happen under rate limiting.
    """
    if df is None or df.empty:
        return False

    # ensure expected columns exist (at least one price column)
    cols = set(map(str, df.columns))
    price_col = None
    for c in ["Close", "Adj Close", "Open"]:
        if c in cols:
            price_col = c
            break
    if price_col is None:
        return False

    # Must have some real numeric values (not all NaN)
    ser = pd.to_numeric(df[price_col], errors="coerce")
    if ser.notna().sum() < 5:   # require at least 5 real rows
        return False

    return True


def download_one(ticker: str) -> pd.DataFrame:
    # explicit settings (also suppresses your "auto_adjust changed default" warning)
    kwargs = dict(
        start=START_DATE,
        end=TODAY,
        auto_adjust=False,
        actions=False,
        progress=False,
        threads=False,
        group_by="column",
    )

    # Some yfinance versions support this; if not, just ignore
    try:
        df = yf.download(ticker, **kwargs, multi_level_index=False)
    except TypeError:
        df = yf.download(ticker, **kwargs)

    df = normalize_df(df)

    if not is_valid_price_df(df):
        raise RetryableDownloadError("Invalid/empty data (rate limit or transient failure)")

    return df


def atomic_write_csv(df: pd.DataFrame, out_path: str) -> None:
    """
    Write safely: write to temp file, then rename.
    Prevents corrupting/emptying an existing good file.
    """
    tmp_path = out_path + ".tmp"
    df.to_csv(tmp_path, index_label="Date")
    os.replace(tmp_path, out_path)


def fetch_data(
    force: bool = False,
    max_age_days: Optional[int] = None,
    max_tries: int = 6,
    base_sleep_s: float = 2.0,
    per_ticker_delay_s: float = 1.0,
) -> Dict[str, str]:
    results: Dict[str, str] = {}

    for t in tickers():
        path = csv_path(t)

        # Decide whether to download this ticker
        should = force or (not os.path.exists(path))
        if (not should) and (max_age_days is not None):
            age_s = time.time() - os.path.getmtime(path)
            if age_s > max_age_days * 86400:
                should = True

        if not should:
            results[t] = "skipped"
            continue

        # Try with backoff, but NEVER write bad data
        ok = False
        last_err = None

        for attempt in range(max_tries):
            try:
                df = download_one(t)
                atomic_write_csv(df, path)
                print(f"[saved] {t} -> {path}")
                results[t] = "ok"
                ok = True
                break
            except RetryableDownloadError as e:
                last_err = str(e)
                sleep_s = (base_sleep_s * (2 ** attempt)) + random.random()
                print(f"[retry] {t}: {last_err}. Sleeping {sleep_s:.2f}s...")
                time.sleep(sleep_s)
            except Exception as e:
                last_err = f"{type(e).__name__}: {e}"
                print(f"[error] {t}: {last_err}")
                break

        if not ok:
            results[t] = f"failed: {last_err or 'unknown'}"
            print(f"[failed] {t}: {results[t]}")

        time.sleep(per_ticker_delay_s + random.random() * 0.6)

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Try to redownload even if CSV exists.")
    parser.add_argument("--max-age-days", type=int, default=None, help="Redownload if older than N days.")
    args = parser.parse_args()

    results = fetch_data(force=args.force, max_age_days=args.max_age_days)

    ok = [t for t, s in results.items() if s == "ok"]
    skipped = [t for t, s in results.items() if s == "skipped"]
    failed = [t for t, s in results.items() if s.startswith("failed")]

    print("\n=== SUMMARY ===")
    print(f"OK: {len(ok)}")
    print(f"Skipped: {len(skipped)}")
    print(f"Failed: {len(failed)}")
    if failed:
        print("Failed tickers:", ", ".join(failed))


if __name__ == "__main__":
    main()
