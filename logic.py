from datetime import datetime

def get_today_name():
    return datetime.today().strftime("%A")

def get_todays_activities(activities):
    today = get_today_name()
    return [activity for activity in activities if today in activity["schedule"]]


def calculate_current_streak(daily_logs):
    streak = 0

    for day in reversed(daily_logs):
        if day["outcome"] == "Completed":
            streak += 1
        else:
            break

    return streak

def calculate_completion_rate(daily_logs):
    completed_days = 0
    total_days = len(daily_logs)

    for day in daily_logs:
        if day["outcome"] == "Completed":
            completed_days += 1

    if total_days == 0:
        return 0

    return (completed_days / total_days) * 100

def calculate_weekly_summary(daily_logs):
    last_7_days = get_last_n_days_logs(daily_logs, 7)

    completed = 0
    missed = 0

    for day in last_7_days:
        if day["outcome"] == "Completed":
            completed += 1
        else:
            missed += 1

    total = len(last_7_days)
    completion_rate = (completed / total) * 100 if total > 0 else 0

    return {
        "total_days": total,
        "completed": completed,
        "missed": missed,
        "completion_rate": completion_rate
    }




def generate_weekly_summary_text(weekly_summary, current_streak):
    completed = weekly_summary["completed"]
    total = weekly_summary["total_days"]
    rate = round(weekly_summary["completion_rate"], 2)

    if current_streak == 0:
        streak_message = "Let’s try to start a new streak tomorrow!"
    elif current_streak == 1:
        streak_message = "You’ve started a new streak. Keep going!"
    else:
        streak_message = f"Great job! You’re on a {current_streak}-day streak."

    return (
        f"This week, you solved LeetCode problems on {completed} out of {total} days.\n"
        f"Your completion rate is {rate}%.\n"
        f"{streak_message}"
    )
