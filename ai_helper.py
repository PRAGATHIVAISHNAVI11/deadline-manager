from datetime import datetime, timedelta

def is_urgent(deadline_str):
    """
    Return True if deadline is within next 6 hours
    """
    try:
        deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        time_left = deadline - datetime.now()
        return time_left.total_seconds() < 6 * 3600
    except Exception as e:
        print("Invalid date format:", e)
        return False
