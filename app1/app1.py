# from flask import Flask, request, render_template
# import pandas as pd
# import io
# import base64
# from utils import (
#     read_data,
#     calculate_statistics,
#     detect_anomalies,
#     plot_anomalies_and_results,
# )

# app = Flask(__name__)


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         file1 = request.files["file1"]
#         df1 = read_data(file1)

#         if "time" not in df1.columns:
#             df1.rename(columns={df1.columns[0]: "time"}, inplace=True)

#         df1["time"] = df1["time"].astype(str).str.extract(r"(\d{2})")[0]
#         df1["time"] = pd.to_datetime(df1["time"], format="%H").dt.strftime("%H:%M")

#         # Calculate original statistics
#         stats = df1.apply(calculate_statistics, axis=1)
#         df_stats = pd.DataFrame(
#             stats.tolist(),
#             columns=[
#                 "weighted_mean",
#                 "mean",
#                 "variance",
#                 "std_dev",
#                 "upper_limit",
#                 "lower_limit",
#             ],
#         )

#         # Detect anomalies based on the new criteria
#         anomalies = df1.apply(detect_anomalies, axis=1)
#         df_anomalies = pd.DataFrame(anomalies.tolist())

#         # Combine dataframes with the modified column order
#         df_result = pd.concat([df1, df_stats], axis=1)
#         df_result_with_anomalies = pd.concat([df_result, df_anomalies], axis=1)

#         # Reorder columns in df_result
#         df_result = df_result[
#             [
#                 "time",
#                 "today",
#                 "yesterday",
#                 "same_day_last_week",
#                 "avg_last_week",
#                 "avg_last_month",
#                 "weighted_mean",
#                 "mean",
#                 "variance",
#                 "std_dev",
#                 "upper_limit",
#                 "lower_limit",
#             ]
#         ]

#         # Reorder columns in df_result_with_anomalies
#         df_result_with_anomalies = df_result_with_anomalies[
#             [
#                 "time",
#                 "today",
#                 "yesterday",
#                 "same_day_last_week",
#                 "weighted_mean",
#                 "today_vs_weighted_mean",
#                 "yesterday_vs_weighted_mean",
#                 "same_day_last_week_vs_weighted_mean",
#             ]
#         ]

#         # Remove any potential duplicate columns
#         df_result = df_result.loc[:, ~df_result.columns.duplicated()]
#         df_result_with_anomalies = df_result_with_anomalies.loc[
#             :, ~df_result_with_anomalies.columns.duplicated()
#         ]

#         # Format tables with two decimal places
#         df_result = df_result.round(2)
#         df_result_with_anomalies = df_result_with_anomalies.round(2)

#         plot_url1 = plot_anomalies_and_results(df_result, df_result_with_anomalies)

#         buf = io.BytesIO()
#         df_result.to_csv(buf, index=False)
#         buf.seek(0)
#         csv_data = base64.b64encode(buf.getvalue()).decode("utf-8")

#         buf_anomalies = io.BytesIO()
#         df_result_with_anomalies.to_csv(buf_anomalies, index=False)
#         buf_anomalies.seek(0)
#         csv_data_anomalies = base64.b64encode(buf_anomalies.getvalue()).decode("utf-8")

#         return render_template(
#             "index.html",
#             tables=[
#                 df_result.to_html(classes="data", float_format="%.2f"),
#                 df_result_with_anomalies.to_html(classes="data", float_format="%.2f"),
#             ],
#             plot_url1=plot_url1,
#             csv_data=csv_data,
#             csv_data_anomalies=csv_data_anomalies,
#         )

#     return render_template("index.html")


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

# from flask import Flask, request, render_template
# import pandas as pd
# import sqlite3
# import io
# import base64
# import matplotlib.pyplot as plt
# from utils import (
#     read_data,
#     calculate_statistics,
#     detect_anomalies,
#     plot_anomalies_and_results,
#     query_sql,
# )

# app = Flask(__name__)

# DATABASE_PATH = "sales_data.db"


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         file1 = request.files["file1"]
#         df1 = read_data(file1)

#         if "time" not in df1.columns:
#             df1.rename(columns={df1.columns[0]: "time"}, inplace=True)

#         df1["time"] = df1["time"].astype(str).str.extract(r"(\d{2})")[0]
#         df1["time"] = pd.to_datetime(df1["time"], format="%H").dt.strftime("%H:%M")

#         # Calculando as estatísticas e adicionando as colunas ao DataFrame
#         stats = df1.apply(lambda row: calculate_statistics(row), axis=1)
#         df_stats = pd.DataFrame(
#             stats.tolist(),
#             columns=[
#                 "weighted_mean",
#                 "mean",
#                 "variance",
#                 "std_dev",
#                 "upper_limit",
#                 "lower_limit",
#             ],
#         )
#         df1 = pd.concat([df1, df_stats], axis=1)

#         # Detectando anomalias e adicionando as colunas ao DataFrame
#         anomalies = df1.apply(
#             lambda row: detect_anomalies(row, row["weighted_mean"]), axis=1
#         )
#         df_anomalies = pd.DataFrame(
#             anomalies.tolist(),
#             columns=[
#                 "today_vs_weighted_mean",
#                 "yesterday_vs_weighted_mean",
#                 "same_day_last_week_vs_weighted_mean",
#             ],
#         )
#         df1 = pd.concat([df1, df_anomalies], axis=1)

#         conn = sqlite3.connect(DATABASE_PATH)
#         df1.to_sql("sales_data", conn, index=False, if_exists="replace")
#         conn.close()

#         plot_url1 = plot_anomalies_and_results(df1, df1)

#         sql_result = query_sql()

#         plt.figure(figsize=(14, 8))
#         plt.plot(sql_result["time"], sql_result["today"], label="Today", color="green")
#         plt.plot(
#             sql_result["time"],
#             sql_result["yesterday"],
#             label="Yesterday",
#             color="orange",
#         )
#         plt.plot(
#             sql_result["time"],
#             sql_result["same_day_last_week"],
#             label="Same Day Last Week",
#             color="blue",
#         )
#         plt.xlabel("Time")
#         plt.ylabel("Values")
#         plt.title("SQL Query Result")
#         plt.legend()
#         plt.grid(True)
#         plt.xticks(rotation=45)
#         plt.tight_layout()

#         buf = io.BytesIO()
#         plt.savefig(buf, format="png")
#         buf.seek(0)
#         plt.close()
#         sql_plot_url = base64.b64encode(buf.getvalue()).decode("utf-8")

#         return render_template(
#             "index.html", plot_url1=plot_url1, sql_plot_url=sql_plot_url
#         )

#     return render_template("index.html")


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, render_template
import pandas as pd
import sqlite3
import io
import base64
import matplotlib.pyplot as plt
from utils import (
    read_data,
    calculate_statistics,
    detect_anomalies,
    plot_anomalies_and_results,
    query_sql,
)

app = Flask(__name__)

DATABASE_PATH = "sales_data.db"


# Define the index route for file upload and processing
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Read the uploaded file
        file1 = request.files["file1"]
        df1 = read_data(file1)

        # Ensure the 'time' column is correctly formatted
        if "time" not in df1.columns:
            df1.rename(columns={df1.columns[0]: "time"}, inplace=True)

        df1["time"] = df1["time"].astype(str).str.extract(r"(\d{2})")[0]
        df1["time"] = pd.to_datetime(df1["time"], format="%H").dt.strftime("%H:%M")

        # Calculate statistics and add columns to the DataFrame
        stats = df1.apply(lambda row: calculate_statistics(row), axis=1)
        df_stats = pd.DataFrame(
            stats.tolist(),
            columns=[
                "weighted_mean",
                "mean",
                "variance",
                "std_dev",
                "upper_limit",
                "lower_limit",
            ],
        )
        df1 = pd.concat([df1, df_stats], axis=1)

        # Detect anomalies and add columns to the DataFrame
        anomalies = df1.apply(
            lambda row: detect_anomalies(row, row["weighted_mean"]), axis=1
        )
        df_anomalies = pd.DataFrame(
            anomalies.tolist(),
            columns=[
                "today_vs_weighted_mean",
                "yesterday_vs_weighted_mean",
                "same_day_last_week_vs_weighted_mean",
            ],
        )
        df1 = pd.concat([df1, df_anomalies], axis=1)

        # Save the DataFrame to SQLite database
        conn = sqlite3.connect(DATABASE_PATH)
        df1.to_sql("sales_data", conn, index=False, if_exists="replace")
        conn.close()

        # Plot anomalies and results, and get the plot URL
        plot_url1 = plot_anomalies_and_results(df1, df1)

        # Query the SQL database
        sql_result = query_sql()

        # Plot the SQL query result
        plt.figure(figsize=(14, 8))
        plt.plot(sql_result["time"], sql_result["today"], label="Today", color="green")
        plt.plot(
            sql_result["time"],
            sql_result["yesterday"],
            label="Yesterday",
            color="orange",
        )
        plt.plot(
            sql_result["time"],
            sql_result["same_day_last_week"],
            label="Same Day Last Week",
            color="blue",
        )
        plt.xlabel("Time")
        plt.ylabel("Values")
        plt.title("SQL Query Result")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot to a buffer and encode it as base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()
        sql_plot_url = base64.b64encode(buf.getvalue()).decode("utf-8")

        # Render the template with the plot URLs
        return render_template(
            "index.html", plot_url1=plot_url1, sql_plot_url=sql_plot_url
        )

    # Render the initial template
    return render_template("index.html")


# Main function to run the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
