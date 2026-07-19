"""
fetch_leetcode.py
Pulls submission calendar via LeetCode's public GraphQL endpoint,
derives streak stats locally, writes data/leetcode.json
"""

import json
import time
from datetime import datetime, timezone
import requests

USERNAME = "RKM_77"
GRAPHQL_URL = "https://leetcode.com/graphql"

QUERY = """
query userProfileCalendar($username: String!) {
  matchedUser(username: $username) {
    userCalendar {
      submissionCalendar
    }
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
"""

HEADERS = {
    "Content-Type": "application/json",
    "Referer": f"https://leetcode.com/{USERNAME}/",
    "User-Agent": "Mozilla/5.0",
}


def fetch_calendar():
    resp = requests.post(
        GRAPHQL_URL,
        json={"query": QUERY, "variables": {"username": USERNAME}},
        headers=HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    matched_user = data.get("data", {}).get("matchedUser")
    if not matched_user:
        raise RuntimeError(f"No user found for '{USERNAME}' - check the username")

    calendar_raw = matched_user["userCalendar"]["submissionCalendar"]
    calendar = json.loads(calendar_raw)  # {"unix_ts_str": count, ...}

    solved_stats = matched_user["submitStats"]["acSubmissionNum"]
    total_solved = next((s["count"] for s in solved_stats if s["difficulty"] == "All"), 0)

    return calendar, total_solved


def to_day(ts: str) -> str:
    return datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%d")


def compute_streaks(calendar: dict):
    active_days = sorted({to_day(ts) for ts, count in calendar.items() if count > 0})
    if not active_days:
        return 0, 0, []

    day_objs = [datetime.strptime(d, "%Y-%m-%d").date() for d in active_days]

    longest = current_run = 1
    for i in range(1, len(day_objs)):
        if (day_objs[i] - day_objs[i - 1]).days == 1:
            current_run += 1
        else:
            current_run = 1
        longest = max(longest, current_run)

    today = datetime.now(timezone.utc).date()
    current_streak = 0
    check_day = today
    active_set = set(day_objs)
    # allow today to be "not yet submitted" without breaking the streak
    if check_day not in active_set:
        check_day = today.fromordinal(today.toordinal() - 1)
    while check_day in active_set:
        current_streak += 1
        check_day = check_day.fromordinal(check_day.toordinal() - 1)

    return current_streak, longest, active_days


def main():
    calendar, total_solved = fetch_calendar()
    current_streak, longest_streak, active_days = compute_streaks(calendar)

    out = {
        "username": USERNAME,
        "total_solved": total_solved,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_active_days": len(active_days),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    with open("data/leetcode.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()