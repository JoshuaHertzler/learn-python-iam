import csv
from datetime import datetime

#Function that loads a CSV and defines a list of row dicts
import csv
import json

def load_users(filename):
    if filename.endswith(".json"):
        with open(filename) as f:
            data = json.load(f)
        # Graph API wraps users in a "value" array
        return data["value"] if isinstance(data, dict) and "value" in data else data
    elif filename.endswith(".csv"):
        users = []
        with open(filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
        return users
    else:
        raise ValueError(f"Unsupported file extension: {filename}")

#Takes in a dict of users and returns department counts
def count_by_dept(users):
    counts = {}
    for user in users:
        dept = user["department"]
        counts[dept] = counts.get(dept, 0) + 1
    return counts

def get_signin_date_string(user):
    # CSV: top-level "lastSignInDateTime"
    # JSON: nested under "signInActivity"
    return (
        user.get("lastSignInDateTime")
        or user.get("signInActivity", {}).get("lastSignInDateTime")
    )

#Function that takes in a single user row and ouputs days since last sign-in
def parse_signin(row):
    try:
        date_str = get_signin_date_string(row)
        if date_str is None:
            return None
        sign_in_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return (datetime.now() - sign_in_date).days
    except (ValueError, KeyError):
        return None

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
    disabled = []
    for user in users:
        enabled = user.get("accountEnabled")
        # accept both: real bool False, or string "False"
        if enabled is False or enabled == "False":
            disabled.append(user)
    return disabled