"""
Day 8 — Modules and JSON

Two new concepts today, both PCEP-relevant and immediately useful:

  1. MODULES — splitting your code into multiple files and importing
     functions across them. Until now everything has been in one
     file; today you'll graduate to a real project shape.

  2. JSON — the format every IAM API actually returns. CSVs are fine
     for spreadsheet exports, but the moment you hit Graph API,
     Okta API, or any AWS SDK call, you're parsing JSON. Today
     you'll read a real Graph-API-shaped export, deal with NESTED
     data, and discover the types you've been faking.

You also get a chance to feel a meaningful difference between data
formats: in CSV, every value is a string ("True", "False", "8"). In
JSON, you get real bools, real numbers, real nested objects. Code
that works on one breaks on the other unless you handle it. Today
you'll see the seam.

I've placed `sample_users.json` in your folder. Open it in VS Code
to see what real Graph-API output looks like. Notice:
  - It's a top-level object with a `value` array — that's how Graph
    paginates. The actual users are inside `value`.
  - `accountEnabled` is now `true`/`false` (real booleans), not strings.
  - `lastSignInDateTime` is NESTED under `signInActivity`.
  - `assignedLicenses` is a list of objects, even when empty.

============================================================
GOAL 1 — Create your first module: `iam_utils.py`
============================================================

Right now your Day 5 functions live in day_05.py and Day 6 has
copies of them. Copy-paste-as-deployment is the original sin of
real codebases. Fix it: extract them into a reusable module.

Steps:

  a. Create a new file in this folder called `iam_utils.py`.

  b. At the top of `iam_utils.py`, put your imports:

         import csv
         from datetime import datetime

  c. Copy these functions into `iam_utils.py` from day_05.py:
         - load_users(filename)
         - count_by_dept(users)
         - parse_signin(row)
         - find_stale(users, threshold_days=90)
         - find_disabled(users)

     Tidy them up while you're at it. Use the try/except version of
     parse_signin from Day 6 (the safer one). Make find_disabled
     return the full user dict, not just the name (the bug we fixed
     on Day 6).

  d. Save iam_utils.py. Don't run it directly — modules don't usually
     have an `if __name__ == "__main__"` block. They're meant to be
     IMPORTED, not executed.

  e. Now in `day_08.py`, at the top, import from your module:

         from iam_utils import load_users, find_stale, find_disabled

     Then test it:

         users = load_users("sample_users.csv")
         print(f"Loaded {len(users)} users")
         print(f"Stale: {len(find_stale(users))}")
         print(f"Disabled: {len(find_disabled(users))}")

     If this runs and prints sensible numbers, you've successfully
     used your own module for the first time. Big moment — this is
     how every real Python project is organized.

  Why this matters: your Day 6 stale_account_detector copied 5
  functions from Day 5. If you fix a bug in Day 5's parse_signin,
  Day 6 still has the broken version. Modules are the cure: define
  the function once, import everywhere.

============================================================
GOAL 2 — Read JSON
============================================================

Add to the top of day_08.py:

    import json

Then try this:

    with open("sample_users.json") as f:
        data = json.load(f)

    print(type(data))        # <class 'dict'>
    print(list(data.keys())) # ['@odata.context', 'value']

`json.load(f)` reads the file and parses it into Python objects:
  - JSON object  →  Python dict
  - JSON array   →  Python list
  - JSON string  →  Python str
  - JSON number  →  Python int or float
  - JSON true/false/null → Python True/False/None

Same shape as your CSV in spirit, but the structure is one level
deeper. The actual users are at `data["value"]`:

    users = data["value"]
    print(len(users))                    # 10
    print(users[0]["displayName"])       # Alice Chen

============================================================
GOAL 3 — Reach into nested data
============================================================

CSV had `lastSignInDateTime` as a top-level column. JSON nests it
inside `signInActivity`. Try:

    user = users[0]
    print(user["signInActivity"]["lastSignInDateTime"])

That's a "chained" dict access — each `[...]` walks one level
deeper. Read it left-to-right.

  Q: What if a user has no signInActivity at all?
  A: KeyError. Real-world Graph data is missing fields all the time.
     The defensive way:

         signin = user.get("signInActivity", {}).get("lastSignInDateTime")

     `user.get("signInActivity", {})` returns the nested dict if it
     exists, or an empty `{}` if not. Then `.get("lastSignInDateTime")`
     on that empty dict safely returns None instead of crashing.

  Build a small loop that prints each user's name and last sign-in,
  using the safe form:

      for user in users:
          signin = user.get("signInActivity", {}).get("lastSignInDateTime")
          print(f"{user['displayName']:<25} {signin}")

  This nested-`.get()` pattern is one of the most-used idioms in
  real API-parsing code. Drill it.

============================================================
GOAL 4 — Spot the type differences
============================================================

JSON has real types. The CSV did not. Run these one at a time:

    csv_users = load_users("sample_users.csv")
    json_users = data["value"]

    print(type(csv_users[0]["accountEnabled"]))   # <class 'str'>
    print(type(json_users[0]["accountEnabled"]))  # <class 'bool'>

    print(csv_users[0]["accountEnabled"] == "True")   # True
    print(json_users[0]["accountEnabled"] == True)    # True
    print(json_users[0]["accountEnabled"] is True)    # True

This is the seam I mentioned. Code written for CSV's string `"True"`
will silently FAIL on JSON's real bool, and vice versa. You'll
work through that in the stretch.

============================================================
GOAL 5 — Write JSON to disk
============================================================

Filter the JSON users to just the disabled ones, then write the
result back out as JSON:

    disabled = [u for u in json_users if not u["accountEnabled"]]
    print(f"{len(disabled)} disabled users")

    with open("disabled_users.json", "w") as f:
        json.dump(disabled, f, indent=2)

    print("Wrote disabled_users.json")

Open the file in VS Code. Notice:
  - The output is human-readable (because of `indent=2`).
  - The full nested structure is preserved — assignedLicenses,
    signInActivity, everything.

Without `indent=2`, json.dump() writes one giant line. Always
pass indent for human-facing output; omit it for machine-to-machine
to save bytes.

============================================================
STRETCH 6 — Make `find_disabled` work on both formats
============================================================

Right now your iam_utils.find_disabled() compares to the string
"False" — that's CSV-only. JSON gives a real bool. Update the
function so it handles BOTH:

    def find_disabled(users):
        disabled = []
        for user in users:
            enabled = user.get("accountEnabled")
            # accept both: real bool False, or string "False"
            if enabled is False or enabled == "False":
                disabled.append(user)
        return disabled

Test it on both inputs:

    print(len(find_disabled(load_users("sample_users.csv"))))   # 2
    print(len(find_disabled(json_users)))                        # 2

Same function, two data sources, same result. That's the payoff
of writing format-aware utilities.

============================================================
STRETCH 7 — Read sign-in date out of either format
============================================================

Add a new helper to iam_utils.py:

    def get_signin_date_string(user):
        # CSV: top-level "lastSignInDateTime"
        # JSON: nested under "signInActivity"
        return (
            user.get("lastSignInDateTime")
            or user.get("signInActivity", {}).get("lastSignInDateTime")
        )

Then update parse_signin to use it. Test on both data sources.

This is the shape of "abstract over the input format" code. It's
how a real CLI tool can accept either a CSV or a JSON file and
produce identical reports.

============================================================
COMMIT
============================================================

    git add iam_utils.py day_08.py sample_users.json disabled_users.json
    git commit -m "feat: day 8 — extract iam_utils module, add JSON support"
    git push

Things you're meeting today:
  - Creating your own module file
  - `from module import name1, name2` (or `import module` + `module.name`)
  - json.load() / json.dump()
  - The `indent=` parameter for human-readable JSON
  - Nested dict access: data[a][b][c]
  - Defensive nested access: d.get(a, {}).get(b)
  - Real types vs stringified types — the data-source seam

Why this matters for IAM:
  Every Microsoft Graph, Okta, AWS, or Falcon API call returns JSON.
  Most return paginated JSON with a `value` (or `data`, or `items`)
  key wrapping the array. Today's patterns are exactly what you'll
  use in Week 5 when we hit the actual Graph API.

Rules of the road:
  - 10-minute stuck rule.
  - Run after each goal.
  - When you create iam_utils.py, save it BEFORE switching to
    day_08.py to import from it. Imports look at disk, not memory.
"""
# Your code below.
from iam_utils import load_users, find_stale, find_disabled
import json

users = load_users("sample_users.csv")
print(f"Loaded {len(users)} users")
print(f"Stale: {len(find_stale(users))}")
print(f"Disabled: {len(find_disabled(users))}")

with open("sample_users.json") as f:
    data = json.load(f)

print(type(data))        # <class 'dict'>
print(list(data.keys())) # ['@odata.context', 'value']

for user in users:
  signin = user.get("signInActivity", {}).get("lastSignInDateTime")
  print(f"{user['displayName']:<25} {signin}")

csv_users = load_users("sample_users.csv")
json_users = data["value"]

print(type(csv_users[0]["accountEnabled"]))   # <class 'str'>
print(type(json_users[0]["accountEnabled"]))  # <class 'bool'>

print(csv_users[0]["accountEnabled"] == "True")   # True
print(json_users[0]["accountEnabled"] == True)    # True
print(json_users[0]["accountEnabled"] is True)    # True

disabled = [u for u in json_users if not u["accountEnabled"]]
print(f"{len(disabled)} disabled users")

with open("disabled_users.json", "w") as f:
    json.dump(disabled, f, indent=2)

print("Wrote disabled_users.json")

print(len(find_disabled(load_users("sample_users.csv"))))   # 2
print(len(find_disabled(json_users)))  