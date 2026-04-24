"""
Day 2 — Dates, types, and days since last sign-in

Scenario:
  Same CSV as yesterday. Today we crack open `lastSignInDateTime`, which is
  currently a useless string, and turn it into something we can do math with.
  By the end you'll know how long it's been since each user last signed in —
  the core data point behind "is this account stale?"

Goal (one at a time, run after each):
  1. At the top, import what you need:  from datetime import datetime
     Inside your loop, parse `row["lastSignInDateTime"]` into a real
     datetime object using:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
     See the format-code tour at the bottom if the %Y%m%d stuff is new.

  2. Print each user's name plus the parsed datetime. Confirm it looks
     different from the raw string (e.g., `2026-04-20 14:32:00`, no T or Z).

  3. For each user, compute `days_since_signin` — the whole number of days
     between now and their last sign-in.
        - Compare against `datetime.now()` (today's date/time).
        - Subtracting two datetimes gives a `timedelta` object.
        - A timedelta has a `.days` attribute. That's your number.

  4. Print one line per user:
        Alice Chen              3 days ago
     Readable spacing is enough. (f-strings can pad: `{name:<25}` left-pads
     a name to 25 chars. Try it if the column alignment bugs you.)

  5. After the loop, print a single summary line naming the MOST stale user
     (highest days_since_signin) and their day count:
        Most stale: Eve Park (172 days ago)
     Hint: track "the worst seen so far" across the loop — two variables,
     updated whenever you find a bigger number. This is the same shape as
     yesterday's counter pattern, but storing a name instead of a count.

Stretch:
  6. Bucket users and print counts:
        active  (< 7 days)
        dormant (7–90 days)
        stale   (> 90 days)

Format-code quick tour:
  %Y = 4-digit year       %H = hour (24h)
  %m = month (01-12)      %M = minute
  %d = day of month       %S = second
  The literal "T" and "Z" in the format string must match the literal
  "T" and "Z" in the input string. strptime is picky — one wrong char
  and it throws ValueError.

Rules of the road:
  - 10-minute stuck rule still applies. Ping me.
  - Run after each step.
  - datetime parsing is a traditional source of pain. Expect at least one
    confusing error. That's normal, not a sign you're doing it wrong.
"""
import csv
from datetime import datetime

with open("sample_users.csv") as f:
   reader = csv.DictReader(f)
   most_stale = 0
   most_stale_name = str()
   active_accounts = 0
   dormant_accounts = 0
   stale_accounts = 0
   for row in reader:
      sign_in_date =  datetime.strptime(row["lastSignInDateTime"], "%Y-%m-%dT%H:%M:%SZ")
      days_since_signin = (datetime.now() - sign_in_date).days
      if days_since_signin > most_stale:
         most_stale_name = row["displayName"]
         most_stale = days_since_signin
      if days_since_signin < 7:
         active_accounts += 1
      elif days_since_signin <= 90:
         dormant_accounts += 1
      else: 
         stale_accounts += 1
      print(f"{row["displayName"]:<25} {days_since_signin}")
   
      
print(f"The most stale account is {most_stale_name} who has not signed in {most_stale} days.")
print(f"Active accounts:{active_accounts}  Dormant Accounts:{dormant_accounts} Stale Accounts:{stale_accounts}")