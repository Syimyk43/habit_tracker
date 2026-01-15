from logic import calculate_current_streak, calculate_completion_rate


def test_calculate_current_streak_basic():
    logs = [
        {"date": "2026-01-10", "outcome": "Missed"},
        {"date": "2026-01-11", "outcome": "Completed"},
        {"date": "2026-01-12", "outcome": "Completed"},
    ]

    assert calculate_current_streak(logs) == 2


def test_calculate_current_streak_zero():
    logs = [
        {"date": "2026-01-10", "outcome": "Completed"},
        {"date": "2026-01-11", "outcome": "Completed"},
        {"date": "2026-01-12", "outcome": "Missed"},
    ]

    assert calculate_current_streak(logs) == 0


def test_calculate_completion_rate():
    logs = [
        {"date": "2026-01-10", "outcome": "Completed"},
        {"date": "2026-01-11", "outcome": "Missed"},
        {"date": "2026-01-12", "outcome": "Completed"},
    ]

    assert round(calculate_completion_rate(logs), 2) == 66.67


def test_calculate_completion_rate_empty():
    assert calculate_completion_rate([]) == 0
