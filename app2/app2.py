import os
from flask import Flask, request, render_template, redirect, send_from_directory
from alert import email_alert
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest
from utils import allowed_file, save_plot_to_image, process_file

app = Flask(__name__)

# Initialize Prometheus Metrics
metrics = PrometheusMetrics(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Define the index route for file upload
@app.route("/", methods=["GET", "POST"])
def index():
    email_sent = False
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], "file.csv")
            file.save(file_path)
            process_file(file_path)
            email_sent = True
            return render_template("index.html", email_sent=email_sent)
    return render_template("index.html", email_sent=email_sent)


# Define the route to serve uploaded files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# Define the route to expose Prometheus metrics
@app.route("/metrics")
def metrics():
    return generate_latest()


# Main function to run the Flask application
if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host="0.0.0.0")
