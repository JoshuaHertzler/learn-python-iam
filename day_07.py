"""
Day 7 — Functions Reps (Review Day)

No new concepts today. This is deliberate practice — eight small,
unrelated function-writing exercises designed to drill the
input → process → return reflex until it's automatic.

You named "forgetting return" as a weak spot on Day 5. Today fixes that.

THE RITUAL FOR EVERY EXERCISE:
  1. Read the spec: what goes in, what comes out.
  2. Write the function.
  3. IMMEDIATELY call it and print the result. No exceptions.
  4. If the print shows None, you forgot return. Fix and re-run.

That third step — calling and printing — is the whole point. Don't
write all eight functions and then test them. Write one, test one.

You can put all eight functions in this single file. Each test call
goes right after the function it tests. Run the file after each
addition. By the end of the file, you'll have ~16 print statements
showing every function works.

============================================================
EXERCISE 1 — `is_admin(job_title)`
============================================================
Input:   a string job_title (e.g., "IAM Engineer", "Recruiter")
Output:  True if the title contains "admin" (case-insensitive),
         False otherwise.
Hint:    "Admin" is found in "Administrator", "Domain Admin",
         "sysadmin". Use .lower() and the `in` operator.

Test:
    print(is_admin("Domain Admin"))          # True
    print(is_admin("Recruiter"))              # False
    print(is_admin("Sysadmin"))               # True

============================================================
EXERCISE 2 — `username_from_upn(upn)`
============================================================
Input:   a UPN like "alice.chen@contoso.com"
Output:  just the part before the "@" — "alice.chen"
Hint:    Strings have a .split() method. Splitting "x@y" on "@"
         gives the list ["x", "y"]. Take index [0].

Test:
    print(username_from_upn("alice.chen@contoso.com"))  # alice.chen
    print(username_from_upn("bob@example.org"))         # bob

============================================================
EXERCISE 3 — `count_enabled(users)`
============================================================
Input:   a list of user dicts (load some from sample_users.csv)
Output:  an integer — how many have accountEnabled == "True"
Note:    you've written this loop before. The new muscle today is
         wrapping it in a function with a clear return.

Test:
    import csv
    with open("sample_users.csv") as f:
        users = list(csv.DictReader(f))
    print(count_enabled(users))    # 8

============================================================
EXERCISE 4 — `filter_by_department(users, department)`
============================================================
Input:   a list of user dicts AND a department name (string)
Output:  a list of users in that department
Hint:    one-line list comprehension is fine here, or a classic
         for-loop with .append() — both are good Python.

Test:
    eng = filter_by_department(users, "Engineering")
    print(len(eng))                 # 3
    for u in eng:
        print(u["displayName"])

============================================================
EXERCISE 5 — `format_user(user, padding=25)`
============================================================
Input:   a single user dict, optional `padding` int (default 25)
Output:  a formatted string like:
            "Alice Chen                <alice.chen@contoso.com>"
         where displayName is left-padded to `padding` characters.
Hint:    f-string with `{name:<{padding}}`. Yes, you can put a
         variable inside the format spec.

Test:
    print(format_user(users[0]))           # default padding 25
    print(format_user(users[0], 10))       # tighter padding

============================================================
EXERCISE 6 — `split_by_status(users)`
============================================================
Input:   a list of user dicts
Output:  RETURN TWO LISTS as a tuple: (enabled_users, disabled_users)
         Yes, a function can return more than one thing — Python
         packs them into a tuple automatically.

Body skeleton:
    enabled = []
    disabled = []
    for user in users:
        ...
    return enabled, disabled

Test (notice the unpacking on the calling side):
    enabled, disabled = split_by_status(users)
    print(f"Enabled: {len(enabled)}, Disabled: {len(disabled)}")

This pattern — returning multiple values, caller unpacks them — is
extremely common. Learn the shape on both sides.

============================================================
EXERCISE 7 — `safe_int(value, default=0)`
============================================================
Input:   any value, plus an optional default
Output:  int(value) if it can be converted, otherwise `default`
Hint:    try / except ValueError. This is the same shape you used
         in Day 6's parse_signin — "if it works return it, if it
         doesn't return a safe default."

Test:
    print(safe_int("42"))           # 42
    print(safe_int("not a number")) # 0
    print(safe_int("nope", -1))     # -1
    print(safe_int(""))             # 0

============================================================
EXERCISE 8 — `summarize(users)`  (composition)
============================================================
Input:   a list of user dicts
Output:  a single string with three lines:
            "Total: 10"
            "Enabled: 8 / Disabled: 2"
            "Departments: 4"

Constraint: this function MUST call your earlier functions —
specifically `split_by_status` (Ex 6) and at least one other.
The lesson is that small functions compose into bigger ones, and
clean returns from the small ones are what make the big one
trivial to write.

Test:
    print(summarize(users))

============================================================
END-OF-DAY REFLEX CHECK
============================================================
Before you stop, scroll through your file and look at every
function you wrote today. For each one, ask:
  - Does it have a `return` statement on the last line that matters?
  - Did I actually CALL it and PRINT the result somewhere?

If any function is missing either, fix it now. That scan IS the
muscle this day is building.

Commit:
    git add day_07.py
    git commit -m "chore: day 7 — functions reps, drilling input/process/return"
    git push

That `chore` prefix is real conventional-commit syntax — it means
"maintenance, not a feature." Worth knowing.
"""
import csv

# Your code below.
##1
def is_admin(job_title):
    admin = "admin"
    if admin in job_title.lower():
        return True
    else: return False

print(is_admin("Administrator"))
##2
def username_from_upn(upn):
    for upns in upn:
        username = upn.split("@")
    return username[0]

print(username_from_upn("Alice.Chen@contoso.com"))

##3
def count_enabled(users):
    count = 0
    for user in users:
        if user["accountEnabled"] == "True":
            count += 1
    return count

with open("sample_users.csv") as f:
    users = list(csv.DictReader(f))
print(count_enabled(users))

#4
def filter_by_department(users, department):
    matches = []
    for user in users:
        if user["department"] == department:
            matches.append(user)
    return matches

eng = filter_by_department(users, "Engineering")
print(len(eng))  # 3

#5
def format_user(user, padding=25):
    return f"{user['displayName']:<{padding}} <{user['userPrincipalName']}>"

print(format_user(users[0], 10)) 

#6
def split_by_status(users):
    enabled = []
    disabled = []
    for user in users:
        if user["accountEnabled"] == "True":
            enabled.append(user)
        else:
            disabled.append(user)
    return enabled, disabled

enabled, disabled = split_by_status(users)
print(f"Enabled: {len(enabled)}, Disabled: {len(disabled)}")

#7
def safe_int(value, default=0):
    try:
        new_int = int(value)
        return  new_int
    except (ValueError):
      return default

print(safe_int("not a number"))

#8
def summarize(users):
    