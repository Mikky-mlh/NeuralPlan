"""
Utility functions - SIDHIKA: Add more helper functions for data processing and validation.
Then write 3 test cases at the bottom to prove it works.
"""
import html

def minutes_to_hours(minutes):
    """Converts 90 → '1h 30m'"""
    minutes = int(minutes)
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return html.escape(f"{hours}h {mins}m")
    else:
        return html.escape(f"{mins}m")

def calculate_time_saved(schedule_df):
    """
    Counts total minutes from cancelled classes.
    Input: DataFrame with columns ["Duration", "Status"]
    Output: Total minutes saved
    """
    if "Status" not in schedule_df.columns or "Duration" not in schedule_df.columns:
        raise ValueError("DataFrame must contain 'Status' and 'Duration' columns")
    
    cancelled = schedule_df[schedule_df["Status"] == "Cancelled"]
    total_minutes = cancelled["Duration"].sum()
    return total_minutes