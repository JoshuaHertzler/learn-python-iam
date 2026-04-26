"""
Day 5 — Functions: refactoring chaos into clean building blocks

Scenario:
  Days 1–4 grew an ad-hoc script: a single `with open(...)` block doing
  CSV reading, datetime parsing, counting, indexing, and filtering all
  in one indented blob. It works, but if a coworker asked "can you give
  me just the stale users from Engineering?" you'd have to copy half the
  script and edit it.

  Functions fix that. Each function is a named, reusable unit with
  EXPLICIT inputs (parameters) and EXPLICIT outputs (return values).
  Tomorrow's mini-project — the Stale Account Detector — will be built
  by composing these functions. So today is the foundation.

  IMPORTANT: write this file from scratch. Don't paste yesterday's blob
  in. Type out the function bodies. The repetition is the point.

Goal (one at a time, run after each):

  1. Define `load_users(filename)` that opens the CSV and returns a
     LIST of row dicts. Skeleton:

         def load_users(filename):
             users = []
             with open(filename) as f:
                 reader = csv.DictReader(f)
                 for row in reader:
                     users.append(row)
             return users

     Then at the bottom of the file:
         users = load_users("sample_users.csv")
         print(len(users))      # 10

     Notice the win: `users` is now a normal list you can re-use as many
     times as you want. The file is opened, read, closed — done.

  2. Define `count_by_department(users)` that takes that list and
     returns a dict like {"Engineering": 3, "Security": 3, ...}.
     Body should be the dict-counter idiom from Day 4, lifted into the
     function. Then call it and print the result:

         counts = count_by_department(users)
         for dept, n in counts.items():
             print(f"{dept:<15} {n}")

     Mental model: `users` goes in, `counts` comes out. Nothing else
     in the program is affected. That's a "pure function" and it's the
     gold standard.

  3. Define `parse_signin(row)` that takes a single user-row dict and
     returns an integer — days since their last sign-in. Reuse your
     Day 2 `strptime` logic. Test it:

         print(parse_signin(users[0]))    # ~6 (Alice)
         print(parse_signin(users[4]))    # ~175 (Eve)

  4. Define `find_stale(users, threshold_days=90)` that returns a
     filtered list of users whose days_since_signin > threshold.
     Use parse_signin() inside it.

     The `threshold_days=90` part is a DEFAULT PARAMETER VALUE — when
     a caller omits the argument, it defaults to 90. Try both:

         stale_90 = find_stale(users)            # uses default 90
         stale_30 = find_stale(users, 30)        # custom threshold
         stale_30 = find_stale(users, threshold_days=30)  # keyword form

     All three calls work. Keyword-argument calls (the third form) are
     more readable for any non-obvious parameter — get in the habit.

  5. Define `build_upn_index(users)` returning a dict keyed by
     userPrincipalName, value = full row. Same idea as Day 4, now in
     a function. Test:

         by_upn = build_upn_index(users)
         print(by_upn["alice.chen@contoso.com"]["department"])

  6. Tie it all together with a `main()` function and the
     `if __name__ == "__main__":` guard at the bottom of the file:

         def main():
             users = load_users("sample_users.csv")
             print(f"Loaded {len(users)} users")
             for dept, n in count_by_department(users).items():
                 print(f"  {dept:<15} {n}")
             stale = find_stale(users, threshold_days=90)
             print(f"\n{len(stale)} stale account(s):")
             for user in stale:
                 days = parse_signin(user)
                 print(f"  {user['displayName']:<25} {days} days")

         if __name__ == "__main__":
             main()

     The `if __name__ == "__main__":` line is Python idiom for "only
     run main() when this file is executed directly, not when it's
     imported by another file." Just learn the shape — the deeper
     reason matters once you start splitting code across files.

Stretch:
  7. Add a docstring to every function. A docstring is a string
     literal as the FIRST line inside the function body — Python
     stores it on the function and tools like help() pick it up:

         def load_users(filename):
             \"\"\"Read a CSV file and return a list of row dicts.\"\"\"
             ...

     After adding, run a Python REPL: `python3 -i day_05.py`
     Then type: help(load_users) — you'll see your docstring.
     This is the same mechanism behind the prompts at the top of
     every day's file.

  8. Add a `find_disabled(users)` function — returns users whose
     accountEnabled == "False". One-liner with a list comprehension.
     Call it from main().

Things you're meeting today:
  - def NAME(params): ... return value
  - Local scope: variables created inside a function vanish when it
    returns. They don't pollute the rest of your program.
  - Default parameter values:  def f(x, y=10):
  - Keyword arguments at call site:  f(x=1, y=2)
  - Returning collections: a function can return a list or dict, and
    the caller treats it like any other list/dict.
  - The `if __name__ == "__main__":` guard.
  - Docstrings (stretch).

Why this matters for IAM specifically:
  Every IAM automation script eventually becomes "load identities, do
  X, write results somewhere." If `load_identities()` is a function,
  you can swap CSV for the Entra Graph API later without touching
  the rest of your code. Functions are how you make code that
  survives a change in data source.

Rules of the road:
  - 10-minute stuck rule.
  - Run after every function you define — call it, print the result.
  - If you find yourself copy-pasting code, that's the signal: pull
    it into a function instead.
"""
import csv
from datetime import datetime

# Your code below.

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

#Function that takes in a single user row and ouputs days since last sign-in
def parse_signin(row):
    sign_in_date = datetime.strptime(row["lastSignInDateTime"], "%Y-%m-%dT%H:%M:%SZ")
    days = (datetime.now() - sign_in_date).days
    return days

def find_stale(users, threshold_days = 90):
    is_stale = []
    for user in users:
        if parse_signin(user) > threshold_days:
            is_stale.append(user)
    return is_stale

def build_upn_index(users):
    users_by_upn = {}
    for user in users:
        users_by_upn[user["userPrincipalName"]] = user
    return users_by_upn

def find_disabled(users):
    disabled_users = []
    for user in users:
        if user["accountEnabled"] == "False":
            disabled_users.append(user["displayName"])
    return disabled_users


def main():
  users = load_users("sample_users.csv")
  print(f"Loaded {len(users)} users")
  for dept, n in count_by_dept(users).items():
    print(f"{dept:<15} {n}")
  stale = find_stale(users, threshold_days=90)
  print(f"\n{len(stale)} stale account(s):")
  for user in stale:
      days = parse_signin(user)
      print(f"  {user['displayName']:<25} {days} days")
  print(f"These users are disabled: {find_disabled(users)}")


if __name__ == "__main__":
  main()