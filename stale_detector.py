import argparse
import json
from iam_utils import load_users, find_stale, find_disabled, parse_signin
from datetime import datetime

def build_report(users, threshold_days):
    lines = []
    lines.append("=" * 60)
    lines.append("Stale Account Detector — Report")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Users scanned: {len(users)}")
    lines.append(f"Stale threshold: {threshold_days} days")
    lines.append("=" * 60)
    lines.append("")
    lines.append("DISABLED ACCOUNTS:")
    for u in find_disabled(users):
        lines.append(f"  {u['displayName']:<25} {u['userPrincipalName']}")
    lines.append("")
    lines.append(f"STALE ACCOUNTS (>{threshold_days} days):")
    for u in find_stale(users, threshold_days):
        days = parse_signin(u)
        lines.append(f"  {u['displayName']:<25} {days} days  ({u['userPrincipalName']})")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Detect stale and disabled accounts in a user export."
    )
    parser.add_argument("--input", required=True,
                        help="Path to user export (.csv or .json)")
    parser.add_argument("--threshold", type=int, default=90,
                        help="Days since last sign-in to consider stale (default: 90)")
    parser.add_argument("--output", default="stale_report.txt",
                        help="Path to write the report (default: stale_report.txt)")
    parser.add_argument("--quiet", action="store_true",
                    help="don't print the report to console")
    parser.add_argument("--format", choices=["txt", "json"], default="txt",
                    help="output format")
    ...
    args = parser.parse_args()

    users = load_users(args.input)
    report = build_report(users, args.threshold)
    if args.format == "json":
        payload = {
            "generated": datetime.now().isoformat(timespec="seconds"),
            "threshold_days": args.threshold,
            "stale": [u["userPrincipalName"] for u in find_stale(users, args.threshold)],
            "disabled": [u["userPrincipalName"] for u in find_disabled(users)],
        }
        with open(args.output, "w") as f:
            json.dump(payload, f, indent=2)
    else:
        with open(args.output, "w") as f:
            f.write(report)
    if not args.quiet:
        print(report)
    print(f"\nReport saved to {args.output}")

if __name__ == "__main__":
    main()