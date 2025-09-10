from datetime import date, timedelta

def start_of_week(d: date) -> date:
    # go back to Monday of this week
    return d - timedelta(days=d.weekday())

def period_anchor_for(habit_type: str, d: date) -> date:
    # daily = same day, weekly = Monday anchor
    return start_of_week(d) if habit_type == "weekly" else d

def consecutive_anchors(anchor_list_desc: list[date]) -> int:
    # count how many anchors in a row (newest first)
    if not anchor_list_desc:
        return 0
    if len(anchor_list_desc) == 1:
        return 1

    step = (anchor_list_desc[0] - anchor_list_desc[1]).days
    step = step if step in (1, 7) else 1

    streak = 1
    for prev, nxt in zip(anchor_list_desc, anchor_list_desc[1:]):
        if (prev - nxt).days == step:
            streak += 1
        else:
            break
    return streak
