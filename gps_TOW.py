from datetime import datetime, timedelta

# Constants
GPS_EPOCH = datetime(1980, 1, 6, 0, 0, 0)  # GPS epoch start time
SECONDS_PER_WEEK = 60 * 60 * 24 * 7        # 604800 seconds per week

def get_gps_time_of_week(current_time=None):
    # Use current UTC time if no specific time is provided
    if current_time is None:
        current_time = datetime.utcnow()

    # Calculate the time difference between the current time and GPS epoch
    time_difference = current_time - GPS_EPOCH
    
    # Calculate total seconds since GPS epoch
    total_seconds = time_difference.total_seconds()
    
    # Calculate GPS week number (integer division)
    gps_week = int(total_seconds // SECONDS_PER_WEEK)
    
    # Calculate GPS time of week (TOW), which is the remainder (modulus) in seconds
    tow = total_seconds % SECONDS_PER_WEEK
    
    return gps_week, tow

# Example usage
if __name__ == "__main__":
    gps_week, tow = get_gps_time_of_week()
    print(f"GPS Week: {gps_week}, Time of Week (TOW): {tow:.2f} seconds")
