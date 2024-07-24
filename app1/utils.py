# import pandas as pd
# import matplotlib.pyplot as plt
# import io
# import base64


# def read_data(file_path):
#     return pd.read_csv(file_path)


# def calculate_statistics(row):
#     historical_values = [
#         row["today"],
#         row["yesterday"],
#         row["same_day_last_week"],
#         row["avg_last_week"],
#         row["avg_last_month"],
#     ]
#     mean = sum(historical_values) / len(historical_values)
#     variance = sum((x - mean) ** 2 for x in historical_values) / (
#         len(historical_values) - 1
#     )
#     std_dev = variance**0.5
#     weighted_mean = (row["avg_last_week"] * 7 + row["avg_last_month"] * 30) / (7 + 30)
#     upper_limit = weighted_mean + 2 * std_dev
#     lower_limit = weighted_mean - 2 * std_dev
#     return (
#         round(weighted_mean, 2),
#         round(mean, 2),
#         round(variance, 2),
#         round(std_dev, 2),
#         round(upper_limit, 2),
#         round(lower_limit, 2),
#     )


# def detect_anomalies(row):
#     threshold = 0.5
#     anomalies = {}
#     weighted_mean = (row["avg_last_week"] * 7 + row["avg_last_month"] * 30) / (7 + 30)
#     anomalies["today_vs_weighted_mean"] = row["today"] < threshold * weighted_mean
#     anomalies["yesterday_vs_weighted_mean"] = (
#         row["yesterday"] < threshold * weighted_mean
#     )
#     anomalies["same_day_last_week_vs_weighted_mean"] = (
#         row["same_day_last_week"] < threshold * weighted_mean
#     )
#     anomalies["weighted_mean"] = round(weighted_mean, 2)
#     return anomalies


# def plot_anomalies_and_results(df_result, df_result_with_anomalies):
#     plt.figure(figsize=(14, 16))

#     # Plot para a primeira tabela
#     plt.subplot(2, 1, 1)
#     series_list = [
#         "today",
#         "yesterday",
#         "same_day_last_week",
#     ]
#     colors = ["green", "orange", "blue"]
#     anomaly_colors = {
#         "today": "green",
#         "yesterday": "orange",
#         "same_day_last_week": "blue",
#     }

#     for i, series in enumerate(series_list):
#         plt.plot(df_result["time"], df_result[series], label=series, color=colors[i])
#         if series != "weighted_mean":
#             anomalies = df_result[
#                 (df_result[series] > df_result["upper_limit"])
#                 | (df_result[series] < df_result["lower_limit"])
#             ]
#             if not anomalies.empty:
#                 plt.scatter(
#                     anomalies["time"],
#                     anomalies[series],
#                     label=f"anomaly_{series}",
#                     s=100,
#                     edgecolor="black",
#                     color=anomaly_colors[series],
#                 )

#     plt.xlabel("Time")
#     plt.ylabel("Values")
#     plt.title("Anomalies detection (First Table)")
#     plt.legend()
#     plt.grid(True)
#     plt.xticks(rotation=45)

#     # Plot para a segunda tabela
#     plt.subplot(2, 1, 2)
#     series_list_anomalies = [
#         "today",
#         "yesterday",
#         "same_day_last_week",
#     ]
#     colors_anomalies = ["green", "orange", "blue"]
#     anomaly_colors_anomalies = {
#         "today": "green",
#         "yesterday": "orange",
#         "same_day_last_week": "blue",
#     }

#     for i, series in enumerate(series_list_anomalies):
#         plt.plot(
#             df_result_with_anomalies["time"],
#             df_result_with_anomalies[series],
#             label=series,
#             color=colors_anomalies[i],
#         )
#         # Adicionar anomalias apenas se forem verdadeiras
#         anomalies = df_result_with_anomalies[
#             (
#                 df_result_with_anomalies["today_vs_weighted_mean"]
#                 & (
#                     df_result_with_anomalies["today"]
#                     == df_result_with_anomalies[series]
#                 )
#             )
#             | (
#                 df_result_with_anomalies["yesterday_vs_weighted_mean"]
#                 & (
#                     df_result_with_anomalies["yesterday"]
#                     == df_result_with_anomalies[series]
#                 )
#             )
#             | (
#                 df_result_with_anomalies["same_day_last_week_vs_weighted_mean"]
#                 & (
#                     df_result_with_anomalies["same_day_last_week"]
#                     == df_result_with_anomalies[series]
#                 )
#             )
#         ]
#         if not anomalies.empty:
#             plt.scatter(
#                 anomalies["time"],
#                 anomalies[series],
#                 label=f"anomaly_{series}",
#                 s=100,
#                 edgecolor="black",
#                 color=anomaly_colors_anomalies[series],
#             )

#     plt.xlabel("Time")
#     plt.ylabel("Values")
#     plt.title("Anomalies detection (Second Table)")
#     plt.legend()
#     plt.grid(True)
#     plt.xticks(rotation=45)
#     plt.tight_layout()

#     buf = io.BytesIO()
#     plt.savefig(buf, format="png")
#     buf.seek(0)
#     plt.close()
#     return base64.b64encode(buf.getvalue()).decode("utf-8")


# import pandas as pd
# import matplotlib.pyplot as plt
# import sqlite3
# import io
# import base64

# DATABASE_PATH = "sales_data.db"


# def read_data(file_path):
#     return pd.read_csv(file_path)


# def calculate_statistics(row):
#     historical_values = [
#         row["today"],
#         row["yesterday"],
#         row["same_day_last_week"],
#         row["avg_last_week"],
#         row["avg_last_month"],
#     ]
#     mean = sum(historical_values) / len(historical_values)
#     variance = sum((x - mean) ** 2 for x in historical_values) / (
#         len(historical_values) - 1
#     )
#     std_dev = variance**0.5
#     weighted_mean = (row["avg_last_week"] * 7 + row["avg_last_month"] * 30) / (7 + 30)
#     upper_limit = weighted_mean + 2 * std_dev
#     lower_limit = weighted_mean - 2 * std_dev
#     return (
#         round(weighted_mean, 2),
#         round(mean, 2),
#         round(variance, 2),
#         round(std_dev, 2),
#         round(upper_limit, 2),
#         round(lower_limit, 2),
#     )


# def detect_anomalies(row, weighted_mean):
#     threshold = 0.5
#     anomalies = {}
#     anomalies["today_vs_weighted_mean"] = row["today"] < threshold * weighted_mean
#     anomalies["yesterday_vs_weighted_mean"] = (
#         row["yesterday"] < threshold * weighted_mean
#     )
#     anomalies["same_day_last_week_vs_weighted_mean"] = (
#         row["same_day_last_week"] < threshold * weighted_mean
#     )
#     return anomalies


# def plot_anomalies_and_results(df_result, df_result_with_anomalies):
#     plt.figure(figsize=(14, 16))

#     # Plot para a primeira tabela
#     plt.subplot(2, 1, 1)
#     series_list = [
#         "today",
#         "yesterday",
#         "same_day_last_week",
#     ]
#     colors = ["green", "orange", "blue"]
#     anomaly_colors = {
#         "today": "green",
#         "yesterday": "orange",
#         "same_day_last_week": "blue",
#     }

#     for i, series in enumerate(series_list):
#         plt.plot(df_result["time"], df_result[series], label=series, color=colors[i])
#         if series != "weighted_mean":
#             anomalies = df_result[
#                 (df_result[series] > df_result["upper_limit"])
#                 | (df_result[series] < df_result["lower_limit"])
#             ]
#             if not anomalies.empty:
#                 plt.scatter(
#                     anomalies["time"],
#                     anomalies[series],
#                     label=f"anomaly_{series}",
#                     s=100,
#                     edgecolor="black",
#                     color=anomaly_colors[series],
#                 )

#     plt.xlabel("Time")
#     plt.ylabel("Values")
#     plt.title("Anomalies detection (First Table)")
#     plt.legend()
#     plt.grid(True)
#     plt.xticks(rotation=45)

#     # Plot para a segunda tabela
#     plt.subplot(2, 1, 2)
#     series_list_anomalies = [
#         "today",
#         "yesterday",
#         "same_day_last_week",
#     ]
#     colors_anomalies = ["green", "orange", "blue"]
#     anomaly_colors_anomalies = {
#         "today": "green",
#         "yesterday": "orange",
#         "same_day_last_week": "blue",
#     }

#     for i, series in enumerate(series_list_anomalies):
#         plt.plot(
#             df_result_with_anomalies["time"],
#             df_result_with_anomalies[series],
#             label=series,
#             color=colors_anomalies[i],
#         )
#         anomalies = df_result_with_anomalies[
#             (
#                 df_result_with_anomalies["today_vs_weighted_mean"]
#                 & (
#                     df_result_with_anomalies["today"]
#                     == df_result_with_anomalies[series]
#                 )
#             )
#             | (
#                 df_result_with_anomalies["yesterday_vs_weighted_mean"]
#                 & (
#                     df_result_with_anomalies["yesterday"]
#                     == df_result_with_anomalies[series]
#                 )
#             )
#             | (
#                 df_result_with_anomalies["same_day_last_week_vs_weighted_mean"]
#                 & (
#                     df_result_with_anomalies["same_day_last_week"]
#                     == df_result_with_anomalies[series]
#                 )
#             )
#         ]
#         if not anomalies.empty:
#             plt.scatter(
#                 anomalies["time"],
#                 anomalies[series],
#                 label=f"anomaly_{series}",
#                 s=100,
#                 edgecolor="black",
#                 color=anomaly_colors_anomalies[series],
#             )

#     plt.xlabel("Time")
#     plt.ylabel("Values")
#     plt.title("Anomalies detection (Second Table)")
#     plt.legend()
#     plt.grid(True)
#     plt.xticks(rotation=45)
#     plt.tight_layout()

#     buf = io.BytesIO()
#     plt.savefig(buf, format="png")
#     buf.seek(0)
#     plt.close()
#     return base64.b64encode(buf.getvalue()).decode("utf-8")


# def query_sql():
#     conn = sqlite3.connect(DATABASE_PATH)
#     query = """
#     SELECT time, today, yesterday, same_day_last_week, avg_last_week, avg_last_month
#     FROM sales_data
#     WHERE today > (SELECT AVG(today) FROM sales_data) + 2 * (SELECT AVG(today) FROM sales_data)
#     """
#     result = pd.read_sql_query(query, conn)
#     conn.close()
#     return result


import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import io
import base64

DATABASE_PATH = "sales_data.db"


# Function to read data from a CSV file
def read_data(file_path):
    return pd.read_csv(file_path)


# Function to calculate statistical metrics
def calculate_statistics(row):
    historical_values = [
        row["today"],
        row["yesterday"],
        row["same_day_last_week"],
        row["avg_last_week"],
        row["avg_last_month"],
    ]
    mean = sum(historical_values) / len(historical_values)
    variance = sum((x - mean) ** 2 for x in historical_values) / (
        len(historical_values) - 1
    )
    std_dev = variance**0.5
    weighted_mean = (row["avg_last_week"] * 7 + row["avg_last_month"] * 30) / (7 + 30)
    upper_limit = weighted_mean + 2 * std_dev
    lower_limit = weighted_mean - 2 * std_dev
    return (
        round(weighted_mean, 2),
        round(mean, 2),
        round(variance, 2),
        round(std_dev, 2),
        round(upper_limit, 2),
        round(lower_limit, 2),
    )


# Function to detect anomalies based on a threshold
def detect_anomalies(row, weighted_mean):
    threshold = 0.5
    anomalies = {}
    anomalies["today_vs_weighted_mean"] = row["today"] < threshold * weighted_mean
    anomalies["yesterday_vs_weighted_mean"] = (
        row["yesterday"] < threshold * weighted_mean
    )
    anomalies["same_day_last_week_vs_weighted_mean"] = (
        row["same_day_last_week"] < threshold * weighted_mean
    )
    return anomalies


# Function to plot anomalies and results
def plot_anomalies_and_results(df_result, df_result_with_anomalies):
    plt.figure(figsize=(14, 16))

    # Plot for the first table
    plt.subplot(2, 1, 1)
    series_list = [
        "today",
        "yesterday",
        "same_day_last_week",
    ]
    colors = ["green", "orange", "blue"]
    anomaly_colors = {
        "today": "green",
        "yesterday": "orange",
        "same_day_last_week": "blue",
    }

    for i, series in enumerate(series_list):
        plt.plot(df_result["time"], df_result[series], label=series, color=colors[i])
        if series != "weighted_mean":
            anomalies = df_result[
                (df_result[series] > df_result["upper_limit"])
                | (df_result[series] < df_result["lower_limit"])
            ]
            if not anomalies.empty:
                plt.scatter(
                    anomalies["time"],
                    anomalies[series],
                    label=f"anomaly_{series}",
                    s=100,
                    edgecolor="black",
                    color=anomaly_colors[series],
                )

    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.title("Anomalies detection (First Table)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    # Plot for the second table
    plt.subplot(2, 1, 2)
    series_list_anomalies = [
        "today",
        "yesterday",
        "same_day_last_week",
    ]
    colors_anomalies = ["green", "orange", "blue"]
    anomaly_colors_anomalies = {
        "today": "green",
        "yesterday": "orange",
        "same_day_last_week": "blue",
    }

    for i, series in enumerate(series_list_anomalies):
        plt.plot(
            df_result_with_anomalies["time"],
            df_result_with_anomalies[series],
            label=series,
            color=colors_anomalies[i],
        )
        anomalies = df_result_with_anomalies[
            (
                df_result_with_anomalies["today_vs_weighted_mean"]
                & (
                    df_result_with_anomalies["today"]
                    == df_result_with_anomalies[series]
                )
            )
            | (
                df_result_with_anomalies["yesterday_vs_weighted_mean"]
                & (
                    df_result_with_anomalies["yesterday"]
                    == df_result_with_anomalies[series]
                )
            )
            | (
                df_result_with_anomalies["same_day_last_week_vs_weighted_mean"]
                & (
                    df_result_with_anomalies["same_day_last_week"]
                    == df_result_with_anomalies[series]
                )
            )
        ]
        if not anomalies.empty:
            plt.scatter(
                anomalies["time"],
                anomalies[series],
                label=f"anomaly_{series}",
                s=100,
                edgecolor="black",
                color=anomaly_colors_anomalies[series],
            )

    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.title("Anomalies detection (Second Table)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return base64.b64encode(buf.getvalue()).decode("utf-8")


# Function to query the SQLite database
def query_sql():
    conn = sqlite3.connect(DATABASE_PATH)
    query = """
    SELECT time, today, yesterday, same_day_last_week, avg_last_week, avg_last_month
    FROM sales_data
    WHERE today > (SELECT AVG(today) FROM sales_data) + 2 * (SELECT AVG(today) FROM sales_data)
    """
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result
