"""
Utility functions - SIDHIKA: Add more helper functions for data processing and validation.
Then write 3 test cases at the bottom to prove it works.
"""

def minutes_to_hours(minutes):
    """Converts 90 → '1h 30m'"""
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}h {mins}m"
    else:
        return f"{mins}m"

def calculate_time_saved(schedule_df):
    """
    Counts total minutes from cancelled classes.
    Input: DataFrame with columns ["Duration", "Status"]
    Output: Total minutes saved
    """
    cancelled = schedule_df[schedule_df["Status"] == "Cancelled"]
    total_minutes = cancelled["Duration"].sum()
    return total_minutes