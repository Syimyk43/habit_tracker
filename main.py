import json
from datetime import date

from logic import get_today_name, get_todays_activities



from logic import (
    calculate_current_streak,
    calculate_completion_rate,
    calculate_weekly_summary,
    generate_weekly_summary_text
)


def get_today_date():
    return date.today().isoformat()

def get_log_for_date(daily_logs, target_date):
    for day in daily_logs:
        if day["date"] == target_date:
            return day
    return None


def ask_today_outcome():
    while True:
        user_input = input("Did you complete this today? (y/n): ").lower()
        if user_input == "y":
            return "Completed"
        elif user_input == "n":
            return "Missed"
        else:
            print("Please enter 'y' or 'n'")


def add_today_log(activity):
    today = get_today_date()
    logs = activity["daily_logs"]

    today_log = get_log_for_date(logs, today)

    if today_log:
        outcome = today_log["outcome"]
        emoji = "✅" if outcome == "Completed" else "❌"

        print(f"You already logged today for {activity['name']}.")
        print(f"Status: {outcome} {emoji}")
        print("Come back tomorrow.")
        return False

    outcome = ask_today_outcome()
    logs.append({
        "date": today,
        "outcome": outcome
    })

    print(f"Saved: {today} → {outcome}")
    return True


def get_last_n_days_logs(daily_logs, n):
    return daily_logs[-n:]


def save_activities_to_file(activities, filename="data.json"):
    with open(filename, "w") as file:
        json.dump(activities, file, indent=4)


def load_activities_from_file(filename="data.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def show_menu():
    print("\nWhat do you want to do?")
    print("1. Log today for an activity")
    print("2. View summary for all activities")
    print("3. Add a new activity")
    print("4. Show today’s planned activities")
    print("5. Exit")


def choose_activity(activities):
    print("\nChoose an activity:")
    for i, activity in enumerate(activities, start=1):
        print(f"{i}. {activity['name']}")

    while True:
        choice = input("Enter number: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(activities):
                return activities[choice - 1]
        print("Invalid choice, try again.")


def add_new_activity(activities):
    name = input("Enter new activity name: ")

    print("Enter days for this activity (comma separated)")
    print("Example: Monday,Wednesday,Friday")
    days_input = input("Days: ")

    schedule = [day.strip().capitalize() for day in days_input.split(",")]

    new_activity = {
        "name": name,
        "schedule": schedule,
        "daily_logs": []
    }

    activities.append(new_activity)
    print(f"Activity '{name}' added with schedule {schedule}.")


def show_all_summaries(activities):
    print("\n===== Activity Summaries =====")

    for activity in activities:
        logs = activity["daily_logs"]

        streak = calculate_current_streak(logs)
        completion_rate = calculate_completion_rate(logs)
        weekly_summary = calculate_weekly_summary(logs)
        summary_text = generate_weekly_summary_text(weekly_summary, streak)

        print("\n----------------------------")
        print(activity["name"])
        print("----------------------------")
        print("Current streak:", streak)
        print("Completion rate:", round(completion_rate, 2), "%")
        print(summary_text)


activities = load_activities_from_file()

if not activities:
    activities = [
        {
            "name": "LeetCode Practice",
            "schedule": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "daily_logs": []
        },
        {
            "name": "Reading",
            "schedule": ["Saturday", "Sunday"],
            "daily_logs": []
        }
    ]


if __name__ == "__main__":
    print("Habit Tracker\n")

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            activity = choose_activity(activities)
            was_saved = add_today_log(activity)

            if was_saved:
                save_activities_to_file(activities)
                print("Saved ✔")


        elif choice == "2":
            show_all_summaries(activities)

        elif choice == "3":
            add_new_activity(activities)
            save_activities_to_file(activities)
            print("Saved ✔")

        elif choice == "4":
            today = get_today_name()
            todays_activities = get_todays_activities(activities)

            print(f"\nToday is {today}")

            if not todays_activities:
                print("No activities planned for today 🎉")
            else:
                print("Today's planned activities:")
                for activity in todays_activities:
                    print("-", activity["name"])

        elif choice == "5":
            save_activities_to_file(activities)
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

