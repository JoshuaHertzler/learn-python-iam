"""
Day 6 — MILESTONE: Stale Account Detector

This is the Week 1 capstone. You're going to compose every concept from
Days 1–5 into a single tool that does a job an IAM engineer would
actually run on a real Friday afternoon:

  "Find every account that's gone stale or been disabled, generate a
   human-readable report, and save it to disk."

You're meeting two genuinely new concepts today, both small and both
PCEP exam topics:

  - Writing files (open(..., "w") + .write())
  - Exception handling with try / except

Everything else is reps on what you already built.

PROJECT SHAPE
=============

Build a script called `stale_account_detector` (this file). When you
run it, it should:

  1. Load users from sample_users.csv
  2. Identify stale accounts (lastSignInDateTime > threshold days ago)
  3. Identify disabled accounts (accountEnabled == "False")
  4. Print a summary to the console
  5. Write a detailed report to `stale_report.txt`

Goals (one at a time, run after each):

  1. Bring your Day 5 functions into this file.
     Copy these directly from day_05.py — paste them at the top:
       - load_users(filename)
       - count_by_department(users)        (rename if needed)
       - parse_signin(row)
       - find_stale(users, threshold_days=90)
       - find_disabled(users)              (your stretch from Day 5)

     Run the file with a quick test at the bottom:
         users = load_users("sample_users.csv")
         print(f"Loaded {len(users)} users")
     Confirm it still works in the new file. This is just rebuilding
     your foundation.

  2. Write a `build_report(users, threshold_days=90)` function that
     returns a multi-line string (the report content). Skeleton:

         def build_report(users, threshold_days=90):
             lines = []
             lines.append("=" * 60)
             lines.append("Stale Account Detector — Report")
             lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
             lines.append(f"Users scanned: {len(users)}")
             lines.append(f"Stale threshold: {threshold_days} days")
             lines.append("=" * 60)
             lines.append("")
             lines.append("DISABLED ACCOUNTS:")
             for user in find_disabled(users):
                 lines.append(f"  {user['displayName']:<25} {user['userPrincipalName']}")
             lines.append("")
             lines.append(f"STALE ACCOUNTS (>{threshold_days} days):")
             for user in find_stale(users, threshold_days):
                 days = parse_signin(user)
                 lines.append(f"  {user['displayName']:<25} {days} days  ({user['userPrincipalName']})")
             return "\n".join(lines)

     The pattern: build a list of strings, then `"\n".join(lines)` to
     glue them together. Print the result and eyeball the formatting.

     New: `"\n".join(lines)` — joins every element with a newline
     between them. Universal pattern for building text output.

  3. Write a `save_report(content, path)` function that writes the
     string to a file:

         def save_report(content, path):
             with open(path, "w") as f:
                 f.write(content)

     Notice: same `with open(...)` shape as reading — but the second
     argument changes from default "r" (read) to "w" (write).
     The `with` block still closes the file for you.

     Test it:
         save_report("hello world", "test.txt")
     Then open test.txt in VS Code and confirm. Delete the test file
     when done (or `rm test.txt`).

     Caution: "w" mode OVERWRITES existing files without warning.
     This is a real-world papercut — we'll treat it carefully later.

  4. Build a `main()` that ties it together:

         def main():
             users = load_users("sample_users.csv")
             report = build_report(users, threshold_days=90)
             print(report)
             save_report(report, "stale_report.txt")
             print(f"\nReport saved to stale_report.txt")

         if __name__ == "__main__":
             main()

     Run it. You should see:
       - The full report printed to your console
       - A new file `stale_report.txt` in your folder

     Open the file in VS Code. That's your tool's output — the thing
     a coworker would actually receive.

  5. Defensive parsing with try / except.

     Right now if `lastSignInDateTime` is missing or malformed for ANY
     user, your whole script crashes. Real exports always have at least
     one bad row. Wrap parse_signin's body in try/except:

         def parse_signin(row):
             try:
                 sign_in_date = datetime.strptime(
                     row["lastSignInDateTime"], "%Y-%m-%dT%H:%M:%SZ"
                 )
                 return (datetime.now() - sign_in_date).days
             except (ValueError, KeyError):
                 return None

     Then update find_stale() to skip None results:

         def find_stale(users, threshold_days=90):
             stale = []
             for user in users:
                 days = parse_signin(user)
                 if days is not None and days > threshold_days:
                     stale.append(user)
             return stale

     Test the safety net: open sample_users.csv, change one user's
     lastSignInDateTime to garbage like `not-a-date`, save, re-run
     your script. It should now print the report without crashing —
     just skipping that user. Restore the CSV when done.

     Concepts:
       - try / except catches errors instead of crashing.
       - You can catch multiple exception types in a tuple: (ValueError, KeyError).
       - `is not None` is the idiomatic way to check "this returned something."
         Don't use `if days != None` — same result, but `is`/`is not` is
         the Pythonic comparison for None.

  6. Commit and push, with a real commit message.

         git add day_06.py stale_report.txt
         git commit -m "feat: stale account detector — Week 1 milestone"
         git push

     Then add a README.md to the repo (next step in stretch #7).

Stretch:
  7. Add a top-level README.md to the repo. Include:
        - Project name and one-paragraph description
        - "What's here" — brief list of the day_NN.py files
        - "Tools" section — describe stale_account_detector
        - "How to run" — `python3 day_06.py`
     This is your repo's front door. Even a small README signals
     professionalism.

  8. Make the threshold configurable from the command line:

         import sys
         threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 90
         report = build_report(users, threshold_days=threshold)

     Then `python3 day_06.py 30` runs with a 30-day threshold,
     `python3 day_06.py` uses the default 90.

     This is your first taste of CLI arguments. We'll do this properly
     with `argparse` in Week 2.

Things you're meeting today:
  - File writing:      with open(path, "w") as f: f.write(content)
  - String joining:    "\n".join(list_of_strings)
  - Exception handling: try / except (ExcType1, ExcType2):
  - is / is not:       identity checks, idiomatic for None
  - Composing your own functions into a `main()` workflow

Why this matters for IAM:
  This is the shape of every internal tool you'll write — load data,
  filter/transform, report. The dataset, the filters, and the output
  format change project to project. The skeleton doesn't.

Rules of the road:
  - 10-minute stuck rule.
  - Run after each goal.
  - If something feels redundant with Day 5, that's GOOD — repetition
    on milestone day is consolidating, not wasted work.
"""
import csv
from datetime import datetime
import sys

# Your code below — start by pasting your Day 5 functions in.
#Function that loads a CSV and defines a list of row dicts
def load_users(filename):
    users = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)
    return users

#Takes in a dict of users and returns department counts
def count_by_dept(users):
    counts = {}
    for user in users:
        dept = user["department"]
        counts[dept] = counts.get(dept, 0) + 1
    return counts

#Function that takes in a single user row and returns days since last sign-in
def parse_signin(row):
    try:
      sign_in_date = datetime.strptime(row["lastSignInDateTime"], "%Y-%m-%dT%H:%M:%SZ")
      return (datetime.now() - sign_in_date).days
    except (ValueError, KeyError):
      return None

#Function that takes in user data and a threshold in days and returns a list of stale users
def find_stale(users, threshold_days = 90):
    stale = []
    for user in users:
      days = parse_signin(user)
      if days is not None and days > threshold_days:
        stale.append(user)
    return stale

#Function that takes in user data and returns a dict of user info keyed on UPN
def build_upn_index(users):
    users_by_upn = {}
    for user in users:
        users_by_upn[user["userPrincipalName"]] = user
    return users_by_upn

#Function that takes in user data and returns a list of disabled users
def find_disabled(users):
    disabled_users = []
    for user in users:
        if user["accountEnabled"] == "False":
            disabled_users.append(user)
    return disabled_users

#FUnction that takes in user data and a threshold in days and returns a multi-line string
def build_report(users, threshold_days=90):
    lines = []
    lines.append("=" * 60)
    lines.append("Stale Account Detector — Report")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Users scanned: {len(users)}")
    lines.append(f"Stale threshold: {threshold_days} days")
    lines.append("=" * 60)
    lines.append("")
    lines.append("DISABLED ACCOUNTS:")
    for user in find_disabled(users):
      lines.append(f"  {user['displayName']:<25} {user['userPrincipalName']}")
    lines.append("")
    lines.append(f"STALE ACCOUNTS (>{threshold_days} days):")
    for user in find_stale(users, threshold_days):
        days = parse_signin(user)
        lines.append(f"  {user['displayName']:<25} {days} days  ({user['userPrincipalName']})")
    return "\n".join(lines)

#Function that takes in report content and a file path and saves the file to disk at that path
def save_report(content, path):
    with open(path, "w") as f:
      f.write(content)


def main():
  users = load_users("sample_users.csv")
  threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 90
  report = build_report(users, threshold_days=threshold)
  save_report(report, "Stale_Users.csv")
  print(report)
  print(f"\nReport saved to stale_report.txt")

if __name__ == "__main__":
            main()