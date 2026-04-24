"""
Day 3 — Lists: collect, sort, slice, filter

Scenario:
  Yesterday's script threw data away as it printed. That's fine for a quick
  summary but useless the moment someone asks "who are the top 3 most stale
  users?" or "just show me Engineering." Today you'll collect rows into a
  list and then do real work on it — the move behind every "give me users
  where X" script you'll ever write.

  Reuse your Day 2 parsing logic (datetime.strptime, days_since_signin).
  You can copy the whole loop over as a starting point.

Goal (one at a time, run after each):
  1. BEFORE the loop, create an empty list:  users = []
     INSIDE the loop, append a two-element tuple of (name, days) to it:
         users.append((row["displayName"], days_since_signin))
     After the loop, print `len(users)`. Should be 10.

  2. Sort the list so the most-stale user is first:
         sorted_users = sorted(users, key=lambda u: u[1], reverse=True)
     Print the whole sorted list. One line per user.

     Don't panic at `lambda`. It's a throwaway function that means
     "given a tuple `u`, compare by its second element (u[1])."
     You'll see this idiom constantly — treat it as a pattern, not a
     concept to master today.

  3. Print ONLY the top 3 most stale, using list slicing:
         sorted_users[:3]
     Format each line like:    Hiro Shah          207 days ago
     (Reuse your f-string padding from Day 2.)

  4. Build a filtered list of users inactive > 90 days. Do it TWICE:
       (a) Classic: new empty list + for-loop + if + .append()
       (b) List comprehension, one line:
             stale_only = [u for u in users if u[1] > 90]
     Confirm both produce the same result. Print one of them.

  5. Build a list of JUST display names (no numbers) with a list
     comprehension:
         names = [u[0] for u in users]
     Print it.

Stretch:
  6. Top 3 most-stale users in Engineering ONLY. Add department as a
     third element of the tuple, filter by department, sort by days,
     slice to 3. Chaining these steps is the whole game.

Things you're meeting today:
  - Tuple  (x, y):  like a list, but fixed length and immutable. Access
                    with [0], [1], etc. Natural fit for "one record."
  - sorted(iter, key=..., reverse=...):  returns a NEW sorted list.
  - list[:n], list[-n:]:  slicing — first n, last n. Does not modify.
  - List comprehension:  [expr for x in iter if cond] — a for-loop
    compressed onto one line. Read it left-to-right the same way.

Rules of the road:
  - 10-minute stuck rule.
  - Run after each step.
  - If list comprehensions feel alien, write the for-loop first, then
    mechanically translate. That translation becomes muscle memory.
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
   stale_list = []
   users = []
   for row in reader:
      sign_in_date =  datetime.strptime(row["lastSignInDateTime"], "%Y-%m-%dT%H:%M:%SZ")
      days_since_signin = (datetime.now() - sign_in_date).days
      users.append((row["displayName"], days_since_signin, row["department"]))
      if days_since_signin > most_stale:
         most_stale_name = row["displayName"]
         most_stale = days_since_signin
      if days_since_signin < 7:
         active_accounts += 1
      elif days_since_signin <= 90:
         dormant_accounts += 1
      else: 
         stale_accounts += 1
         stale_list.append((row["displayName"], days_since_signin, row["department"]))

stale_only = [u for u in users if u[1] > 90]
names = [u[0] for u in users]
#      print(f"{row["displayName"]:<25} {days_since_signin}")
sorted_users = sorted(users, key=lambda u: u[1], reverse=True)
stale_engineers = []
for name, days, department in users:
   if department == "Engineering":
      stale_engineers.append((name, days))

sorted_engineers = sorted(stale_engineers, key=lambda u: u[1], reverse=True)
for name, days in sorted_engineers[:3]:
   print(f"{name:<25} {days:<25}")