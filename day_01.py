"""
Day 1 — Read and summarize a user export

Scenario:
  You've been handed `sample_users.csv` — a simulated export from Entra ID.
  Your task is to write a script that reads the file and prints a quick
  summary so an IAM engineer can eyeball it before running deeper reports.

Goal (in order — do them one at a time, run after each):
  1. Open `sample_users.csv` and read it using the built-in `csv` module.
     Hint: `csv.DictReader` gives you each row as a dict keyed by header name.
  2. Print the total number of user rows.
  3. Print each user's displayName and userPrincipalName, one per line,
     in the format:   Alice Chen  <alice.chen@contoso.com>
  4. Print how many accounts are enabled vs. disabled.
     Note: the CSV column `accountEnabled` is the string "True" or "False".
     You'll need to compare it as a string or convert it — your call, but
     think about which is more honest.

Rules of the road:
  - Write it, run it, break it. `python3 day_01.py` from this directory.
  - If you get stuck for more than ~10 minutes on any step, stop and ping me.
    That is the rule. The roadblock-and-disappear pattern ends here.
  - Don't look things up on Stack Overflow first. Try, then ask me.

Stretch (only if the above felt too easy):
  5. Print a per-department count, e.g.   Engineering: 3

---
"""
import csv

with open("sample_users.csv") as f:
    reader = csv.DictReader(f)
    row_total = 0
    enabled_accounts = 0
    disabled_accounts = 0
    engineering_dept = 0
    security_dept = 0
    finance_dept = 0
    hr_dept = 0

    for row in reader:
        print(f"{row['displayName']} <{row['userPrincipalName']}>")
        row_total += 1
        if row["accountEnabled"] == "True":
            enabled_accounts += 1
        else: 
            disabled_accounts +=1
        if row["department"] == "Engineering":
            engineering_dept += 1
        elif row["department"] == "Security":
            security_dept += 1
        elif row["department"] == "Finance":
            finance_dept += 1
        elif row["department"] == "HR":
            hr_dept +=1
    print(row_total)
    print(f"Enabled accounts: {enabled_accounts} Disabled accounts:{disabled_accounts}")
    print(f"Engineering:{engineering_dept}, Security:{security_dept}, Finance:{finance_dept}, HR:{hr_dept}")