import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
from matplotlib.dates import HourLocator, DateFormatter
from flask import current_app as app
from prometheus_client import Counter, Gauge
from alert import email_alert

# Define custom metrics
anomaly_counter = Counter(
    "anomalies_detected", "Number of anomalies detected", ["status"]
)
hourly_values = Gauge("hourly_values", "Hourly summed values", ["status", "timestamp"])
anomaly_values = Gauge("anomaly_values", "Anomaly values", ["status", "timestamp"])


# Check if the file is allowed (CSV)
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"csv"}


# Save plot to image and return the path and base64 encoded string
def save_plot_to_image(df, status, value_column, filename="plot.png"):
    plt.figure(figsize=(18, 10))

    plt.plot(df["hour"], df[value_column], label=status, alpha=0.7)

    anomalies = df[df[f"anomaly_{value_column}"].notnull()]
    plt.scatter(
        anomalies["hour"],
        anomalies[value_column],
        label=f"anomaly_{status}",
        color="red",
    )

    plt.xlabel("Hour of Day")
    plt.ylabel("Values")
    plt.title(f"Hourly Data with Anomalies for {status}")
    plt.legend()
    plt.grid(True)

    ax = plt.gca()
    ax.xaxis.set_major_locator(HourLocator(interval=1))
    ax.xaxis.set_major_formatter(DateFormatter("%H"))
    ax.set_xlim([0, 23])
    plt.xticks(range(24), [f"{h:02d}h" for h in range(24)], rotation=45)
    ax.spines["top"].set_visible(False)

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    plt.savefig(image_path)
    plt.close()

    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    return image_path, image_base64


# Process the uploaded CSV file and detect anomalies
def process_file(file_path):
    df = pd.read_csv(file_path)

    if "time" not in df.columns:
        raise ValueError(
            "The DataFrame does not have a column named 'time'. Check the format of your CSV file."
        )

    df["time"] = pd.to_datetime(df["time"], format="%Hh %M", errors="coerce")
    df["timestamp"] = df["time"].apply(lambda x: int(x.timestamp()))

    df["hour"] = df["time"].dt.hour

    value_column = "f0_" if "f0_" in df.columns else "count"

    anomaly_results = {}

    for status in ["failed", "denied", "reversed"]:
        hourly_sums = (
            df[df["status"] == status].groupby("hour")[value_column].sum().reset_index()
        )

        mean_value = hourly_sums[value_column].mean()
        std_dev = hourly_sums[value_column].std()

        hourly_sums[f"anomaly_{value_column}"] = hourly_sums.apply(
            lambda row: (
                row[value_column]
                if (row[value_column] - mean_value) / std_dev > 0.7
                else None
            ),
            axis=1,
        )

        for _, row in hourly_sums.iterrows():
            hour = int(row["hour"])

            timestamp = (
                pd.Timestamp.now()
                .replace(hour=hour, minute=0, second=0, microsecond=0)
                .timestamp()
            )
            value = row[value_column]

            hourly_values.labels(status=status, timestamp=int(timestamp)).set(value)

            anomaly = row[f"anomaly_{value_column}"]
            if anomaly is not None and not pd.isnull(anomaly):
                anomaly_values.labels(status=status, timestamp=int(timestamp)).set(
                    anomaly
                )
                anomaly_counter.labels(status=status).inc()

        hourly_sums["hour"] = hourly_sums["hour"].apply(lambda h: f"{h:02d}h")
        anomaly_results[status] = hourly_sums

    image_filenames = []
    image_base64_list = []
    email_body_parts = []

    # Generate plots and prepare email content
    for status in ["denied", "failed", "reversed"]:
        image_filename, image_base64 = save_plot_to_image(
            anomaly_results[status], status, value_column, filename=f"plot_{status}.png"
        )
        image_filenames.append(image_filename)
        image_base64_list.append(image_base64)

        anomalies_df = anomaly_results[status][
            anomaly_results[status][f"anomaly_{value_column}"].notnull()
        ]
        anomalies_df = anomalies_df.drop(columns=[f"anomaly_{value_column}"])
        anomalies_data = anomalies_df.to_string(index=False)
        email_body_parts.append(f"Anomalies for {status}:\n{anomalies_data}")

    email_body = "\n\n".join(email_body_parts)

    email_alert(
        "Anomaly Report", email_body, "danielcf147@gmail.com", image_base64_list
    )

    return image_filenames
