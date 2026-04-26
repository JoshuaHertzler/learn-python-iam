"""
Day 4 — Dicts: lookup, counting, and the death of the hardcoded counter

Scenario:
  Day 1 had this gem:
      engineering_count = 0
      security_count = 0
      finance_count = 0
      hr_count = 0
      ...elif row["department"] == "Engineering": engineering_count += 1...

  That code is brittle. Add a "Marketing" user to the CSV and your script
  silently undercounts. Real exports have departments you didn't anticipate.
  Today you'll replace that whole pattern with a single dict that grows on
  demand — the universal "count things by category" move.

  You'll also build the IAM bread-and-butter operation: looking up a user
  by their UPN, in O(1).

  Reuse your CSV-reading scaffolding from earlier days. You can copy the
  `with open(...)` block over and start from there.

Goal (one at a time, run after each):
  1. Build a department-count dict the right way.
     BEFORE the loop:
         dept_counts = {}
     INSIDE the loop:
         dept = row["department"]
         dept_counts[dept] = dept_counts.get(dept, 0) + 1

     Read that last line out loud. "Set dept_counts[dept] to its current
     value (or 0 if it doesn't exist yet) plus 1." That's the whole idiom.

     After the loop, iterate and print:
         for dept, count in dept_counts.items():
             print(f"{dept:<15} {count}")

     Compare your output to Day 1's hardcoded version. Same numbers,
     way less code, and adding a new department requires zero changes.

  2. Build a UPN → user lookup dict.
     BEFORE the loop:
         users_by_upn = {}
     INSIDE the loop:
         users_by_upn[row["userPrincipalName"]] = row

     After the loop, look up a specific user and print their info:
         alice = users_by_upn["alice.chen@contoso.com"]
         print(alice["displayName"], alice["department"], alice["jobTitle"])

  3. Defensive lookup. Try this AFTER the loop:
         missing = users_by_upn["nobody@contoso.com"]

     You'll get a KeyError. That's Python telling you the key isn't there.
     Now do it the safe way:
         missing = users_by_upn.get("nobody@contoso.com")
         print(missing)   # prints None instead of crashing

     Or supply a default:
         missing = users_by_upn.get("nobody@contoso.com", "USER NOT FOUND")

     The .get() pattern is one of the most-used dict methods in real code,
     especially when parsing API responses where a field might be absent.

  4. Iterate the dict three different ways. Run each and observe:
         for upn in users_by_upn:           print(upn)            # keys
         for user in users_by_upn.values(): print(user["displayName"])
         for upn, user in users_by_upn.items(): print(upn, "->", user["jobTitle"])

     `.items()` is the one you'll use 90% of the time.

  5. Membership check with `in`.
         if "alice.chen@contoso.com" in users_by_upn:
             print("Alice exists")
         if "ghost@contoso.com" not in users_by_upn:
             print("Ghost does not")

     This is how you'd guard a downstream API call: "before I try to disable
     this account, does it even exist in our directory?"

Stretch:
  6. Build a `users_by_department` dict where each key is a department name
     and each value is a LIST of displayNames in that department. Result
     should look like:
         {
           "Engineering": ["Alice Chen", "Bob Martinez", "Imani Webb"],
           "Security":    ["Carla Nguyen", "David Okafor", "Jamal Reyes"],
           ...
         }

     Hint: you'll combine .get() with .append(), or use setdefault().
     Print one department's list, e.g. all Engineering names.

  7. (Only if you want a taste of the stdlib.) Replace your manual dept
     counter from goal 1 with `collections.Counter`:
         from collections import Counter
         dept_counts = Counter(row["department"] for row in rows)
     Then `dept_counts.most_common(3)` gives you the top 3 departments by
     headcount. We'll lean on this kind of stdlib shortcut more in week 2.

Things you're meeting today:
  - dict literal:        {"key": value}
  - dict access:         d[key]  (raises KeyError if missing)
  - dict safe access:    d.get(key)            -> None if missing
                         d.get(key, default)   -> default if missing
  - dict update:         d[key] = value        (creates or replaces)
  - dict iteration:      .keys(), .values(), .items()
  - membership:          key in d, key not in d
  - nested structure:    dict of dicts, dict of lists — the bread and butter
                         of representing real-world data

Why dicts matter for IAM specifically:
  Almost every IAM API hands you data as JSON, which becomes Python dicts.
  Looking up "what groups is this user in?" or "is this UPN active?" is
  always a dict access. Building a UPN -> user map once, then doing many
  fast lookups, is the foundation of every reconciliation script you'll
  ever write.

Rules of the road:
  - 10-minute stuck rule.
  - Run after each step.
  - Try the unsafe access (goal 3) before the safe one. Crashing on purpose
    once is the fastest way to internalize why .get() exists.
"""
# Your code below.
import csv
from datetime import datetime
from collections import Counter

with open("sample_users.csv") as f:
   reader = csv.DictReader(f)
   dept_counts = {}
   users_by_upn = {}
   users_by_dept = {}
   for row in reader:
      dept = row["department"]
      name = row["displayName"]
      dept_counts[dept] = dept_counts.get(dept, 0) + 1
      users_by_upn[row["userPrincipalName"]] = row
      if dept not in users_by_dept:
          users_by_dept[dept] = []
      users_by_dept[dept].append(name)
missing = users_by_upn.get("nobody@contoso.com")
print(missing)
alice = users_by_upn["alice.chen@contoso.com"]
print(alice["displayName"], alice["department"], alice["jobTitle"])
print(users_by_dept)


for upn in users_by_upn:
    print(upn)
for user in users_by_upn.values(): 
    print(user["displayName"])
for upn, user in users_by_upn.items():
    print(upn, "->", user["jobTitle"])

if "alice.chen@contoso.com" in users_by_upn:
    print("Alice exists")
if "ghost@contoso.com" not in users_by_upn:
    print("Ghost does not")
