#!/usr/bin/env python3
"""
Export active open mics from Supabase for monthly Instagram verification.
"""

import argparse
import os
import sys

import pandas as pd
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(description="Export active mics for monthly Instagram verification")
    parser.add_argument("--output", default="monthly_verification_mics.csv")
    parser.add_argument("--json-output", help="Optional JSON output path for the same exported rows")
    parser.add_argument("--table", default="open_mics_historical")
    args = parser.parse_args()

    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("Missing SUPABASE_URL or SUPABASE_KEY")
        sys.exit(1)

    from supabase import create_client

    supabase = create_client(url, key)
    rows = []
    page_size = 1000
    start = 0

    while True:
        end = start + page_size - 1
        response = (
            supabase.table(args.table)
            .select("*")
            .eq("active", True)
            .range(start, end)
            .execute()
        )
        page = response.data or []
        rows.extend(page)
        if len(page) < page_size:
            break
        start += page_size

    if not rows:
        print("No active mics found")
        sys.exit(1)

    df = pd.DataFrame(rows)
    df.to_csv(args.output, index=False)
    print(f"Exported {len(df)} active mics to {args.output}")
    if args.json_output:
        df.to_json(args.json_output, orient="records", indent=2)
        print(f"Exported {len(df)} active mics to {args.json_output}")


if __name__ == "__main__":
    main()
