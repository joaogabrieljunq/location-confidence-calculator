import pandas as pd


def calculate_confidence_for_interval(data, start_time, end_time, sub_interval="1H"):
    filtered_data = data[
        (data["Local Date & Time"] >= start_time)
        & (data["Local Date & Time"] <= end_time)
    ].copy()
    if filtered_data.empty:
        return pd.DataFrame(
            columns=["Start Time", "End Time", "Dominant State", "Confidence (%)"]
        )

    filtered_data.set_index("Local Date & Time", inplace=True)
    resampled = filtered_data.resample(sub_interval).apply(
        lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown"
    )
    confidence = filtered_data.resample(sub_interval)["State"].apply(
        lambda x: 100 * (x.value_counts().max() / len(x)) if len(x) > 0 else 0
    )

    # Update: Handle no clear mode by defaulting to "Unknown"
    dominant_state_mode = resampled["State"].mode()
    dominant_state = (
        dominant_state_mode.iloc[0] if len(dominant_state_mode) == 1 else "Unknown"
    )
    overall_confidence = (
        filtered_data["State"].value_counts().max() / len(filtered_data)
    ) * 100

    result = pd.DataFrame(
        {
            "Start Time": [start_time],
            "End Time": [end_time],
            "Dominant State": [dominant_state],
            "Confidence (%)": [overall_confidence],
        }
    )

    return result
