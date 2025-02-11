import pandas as pd


def calculate_confidence_for_interval(data, start_time, end_time, time_gap_minutes=30):
    """
    Calculates dominant state and confidence level for dynamic intervals within a specified time range.

    Improved Logic:
      - Filter data between start_time and end_time.
      - Sort data by 'Local Date & Time'.
      - Group consecutive records into intervals if the gap between them is <= time_gap_minutes.
      - For each interval, determine the dominant state (majority vote) and compute confidence as
        the percentage of records that agree with that dominant state.

    Parameters:
      data (pd.DataFrame): DataFrame containing at least 'Local Date & Time' and 'State' columns.
      start_time (pd.Timestamp): Lower bound of the time window.
      end_time (pd.Timestamp): Upper bound of the time window.
      time_gap_minutes (int): Maximum gap (in minutes) between consecutive points to be considered
                              part of the same interval.

    Returns:
      pd.DataFrame: A report with columns ["Start Time", "End Time", "Dominant State", "Confidence (%)"]
    """

    # Filter the data for the specified time range
    filtered_data = data[
        (data["Local Date & Time"] >= start_time)
        & (data["Local Date & Time"] <= end_time)
    ].copy()

    if filtered_data.empty:
        return pd.DataFrame(
            columns=["Start Time", "End Time", "Dominant State", "Confidence (%)"]
        )

    # Ensure data is sorted chronologically
    filtered_data.sort_values("Local Date & Time", inplace=True)

    # Define the allowed time gap as a pandas Timedelta
    time_gap = pd.Timedelta(minutes=time_gap_minutes)

    # Group data into intervals based on time gaps between consecutive records
    intervals = []
    current_interval = []
    for _, row in filtered_data.iterrows():
        if not current_interval:
            current_interval.append(row)
        else:
            last_time = current_interval[-1]["Local Date & Time"]
            if (row["Local Date & Time"] - last_time) <= time_gap:
                current_interval.append(row)
            else:
                # Finish the current interval and start a new one
                intervals.append(pd.DataFrame(current_interval))
                current_interval = [row]
    if current_interval:
        intervals.append(pd.DataFrame(current_interval))

    # For each interval, determine the dominant state and its confidence level.
    results = []
    for interval_df in intervals:
        interval_start = interval_df["Local Date & Time"].min()
        interval_end = interval_df["Local Date & Time"].max()
        state_counts = interval_df["State"].value_counts()

        # In case there is no valid state information, default to "Unknown" and 0% confidence.
        if state_counts.empty:
            dominant_state = "Unknown"
            confidence = 0.0
        else:
            dominant_state = state_counts.idxmax()
            confidence = 100.0 * state_counts.max() / state_counts.sum()

        results.append(
            {
                "Start Time": interval_start,
                "End Time": interval_end,
                "Dominant State": dominant_state,
                "Confidence (%)": round(confidence, 2),
            }
        )

    return pd.DataFrame(results)
