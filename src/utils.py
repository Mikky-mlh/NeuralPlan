import html

def minutes_to_hours(minutes):
    """Converts 90 → '1h 30m'"""
    minutes = int(minutes)
    hours = minutes // 60
    mins = minutes % 60
    result = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
    return html.escape(result)

def calculate_time_saved(schedule_df):
    """Sums minutes from cancelled classes"""
    if "Status" not in schedule_df.columns or "Duration" not in schedule_df.columns:
        raise ValueError("DataFrame must contain 'Status' and 'Duration' columns")
    
    cancelled = schedule_df[schedule_df["Status"] == "Cancelled"]
    total_minutes = cancelled["Duration"].sum()
    return total_minutes