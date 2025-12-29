# A simple utility file for Teammate B to practice logic
def minutes_to_hours(minutes):
    """Converts minutes to a string like '1h 30m'"""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"